#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 hou.mon // @ihouman on X (Houman Shekarchi)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED

"""
MLX Quantize & Convert GUI v2.0

A streamlined tool for converting machine learning models to Apple's MLX format
with optional quantization. Simplified UI with robust error handling.

Requirements:
  pip install -U mlx-lm
"""

import os
import sys
import json
import shutil
import threading
import subprocess
import shlex
import platform
import time
from datetime import datetime
from pathlib import Path
from tkinter import (Tk, Frame, Label, Entry, Button, Checkbutton, Text, 
                    StringVar, BooleanVar, IntVar, BOTH, X, Y, EW, W, E, 
                    END, LEFT, RIGHT, BOTTOM, TOP, DISABLED, NORMAL)
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

# Application metadata
APP_TITLE = "MLX Quantize & Convert"
APP_VERSION = "2.0"

# Default configuration values
DEFAULT_OUTPUT_BASE = str(Path.home() / "MLX_Models")
DEFAULT_CONFIG_PATH = str(Path.home() / ".mlx_quant_gui.json")

# Quantization presets: (bits, group_size, dtype)
PRESET_CONFIGS = {
    "Fast & Good (4-bit)": ("4", "64", "float16"),
    "High Quality (8-bit)": ("8", "64", "float16"),
    "Tiny Size (2-bit)": ("2", "128", "bfloat16"),
    "Balanced (6-bit)": ("6", "64", "float16"),
    "Custom": (None, None, None),
}

class MLXQuantizeApp(Tk):
    """Streamlined MLX conversion tool with improved UI and error handling."""
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        
        self.title(f"{APP_TITLE} v{APP_VERSION}")
        self.geometry("900x750")
        self.minsize(800, 600)
        
        # Initialize variables
        self._init_variables()
        
        # Background processing
        self.current_process = None
        self.worker_thread = None
        
        # Build UI
        self._build_ui()
        
        # Set initial state
        self._update_ui_state()
        
        # Log startup
        self._log("Application ready. Ensure mlx-lm is installed: pip install -U mlx-lm")
        
    def _init_variables(self):
        """Initialize all state variables."""
        # Source
        self.source_path = StringVar(value="")
        self.source_type = StringVar(value="auto")  # auto, local, hf
        
        # Output
        self.output_base = StringVar(value=DEFAULT_OUTPUT_BASE)
        self.auto_timestamp = BooleanVar(value=True)
        
        # Quantization
        self.preset = StringVar(value="Fast & Good (4-bit)")
        self.enable_quant = BooleanVar(value=True)
        self.q_bits = StringVar(value="4")
        self.q_group = StringVar(value="64")
        self.dtype = StringVar(value="float16")
        
        # Advanced
        self.show_advanced = BooleanVar(value=False)
        self.trust_remote = BooleanVar(value=True)
        self.hf_offline = BooleanVar(value=False)
        self.dry_run = BooleanVar(value=False)
        self.wired_memory = StringVar(value="96000")
        
    def _build_ui(self):
        """Build the user interface."""
        # Main container with padding
        main = ttk.Frame(self, padding="10")
        main.pack(fill=BOTH, expand=True)
        
        # Title
        title = ttk.Label(main, text="MLX Model Converter", 
                         font=('Helvetica', 16, 'bold'))
        title.pack(pady=(0, 10))
        
        # Source section
        self._build_source_section(main)
        
        # Output section  
        self._build_output_section(main)
        
        # Quantization section
        self._build_quant_section(main)
        
        # Advanced section (collapsible)
        self._build_advanced_section(main)
        
        # Log section (expandable)
        self._build_log_section(main)
        
        # Main action buttons at bottom (most prominent)
        self._build_action_buttons(main)
        
    def _build_source_section(self, parent):
        """Build source selection section."""
        frame = ttk.LabelFrame(parent, text="1. Select Model Source", padding="10")
        frame.pack(fill=X, pady=(0, 10))
        
        # Input field
        ttk.Label(frame, text="Model Path or HuggingFace ID:").grid(
            row=0, column=0, sticky=W, pady=(0, 5))
        
        input_frame = ttk.Frame(frame)
        input_frame.grid(row=1, column=0, sticky=EW)
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.source_entry = ttk.Entry(input_frame, textvariable=self.source_path)
        self.source_entry.grid(row=0, column=0, sticky=EW, padx=(0, 5))
        
        ttk.Button(input_frame, text="Browse Local...", 
                  command=self._browse_source).grid(row=0, column=1)
        
        # Examples
        examples = ttk.Label(frame, 
            text="Examples: /path/to/model, meta-llama/Llama-3.2-3B, model.safetensors",
            font=('Helvetica', 10), foreground='gray')
        examples.grid(row=2, column=0, sticky=W, pady=(5, 0))
        
        frame.grid_columnconfigure(0, weight=1)
        
    def _build_output_section(self, parent):
        """Build output configuration section."""
        frame = ttk.LabelFrame(parent, text="2. Configure Output", padding="10")
        frame.pack(fill=X, pady=(0, 10))
        
        # Output base directory
        ttk.Label(frame, text="Output Base Directory:").grid(
            row=0, column=0, sticky=W, pady=(0, 5))
        
        output_frame = ttk.Frame(frame)
        output_frame.grid(row=1, column=0, sticky=EW)
        output_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_base).grid(
            row=0, column=0, sticky=EW, padx=(0, 5))
        
        ttk.Button(output_frame, text="Browse...", 
                  command=self._browse_output).grid(row=0, column=1, padx=(0, 5))
        
        ttk.Button(output_frame, text="Open", 
                  command=self._open_output).grid(row=0, column=2)
        
        # Auto-timestamp option
        ttk.Checkbutton(frame, text="Add timestamp to output folder (prevents conflicts)",
                       variable=self.auto_timestamp).grid(
            row=2, column=0, sticky=W, pady=(5, 0))
        
        frame.grid_columnconfigure(0, weight=1)
        
    def _build_quant_section(self, parent):
        """Build quantization settings section."""
        frame = ttk.LabelFrame(parent, text="3. Quantization Settings", padding="10")
        frame.pack(fill=X, pady=(0, 10))
        
        # Enable quantization
        ttk.Checkbutton(frame, text="Enable Quantization",
                       variable=self.enable_quant,
                       command=self._update_ui_state).pack(anchor=W)
        
        # Preset selector
        preset_frame = ttk.Frame(frame)
        preset_frame.pack(fill=X, pady=(5, 0))
        
        ttk.Label(preset_frame, text="Preset:").pack(side=LEFT, padx=(0, 5))
        
        self.preset_combo = ttk.Combobox(preset_frame, textvariable=self.preset,
                                         values=list(PRESET_CONFIGS.keys()),
                                         state="readonly", width=20)
        self.preset_combo.pack(side=LEFT, padx=(0, 10))
        self.preset_combo.bind("<<ComboboxSelected>>", self._on_preset_change)
        
        # Custom settings (shown when Custom is selected)
        self.custom_frame = ttk.Frame(frame)
        
        ttk.Label(self.custom_frame, text="Bits:").grid(row=0, column=0, sticky=E, padx=(0, 5))
        ttk.Combobox(self.custom_frame, textvariable=self.q_bits,
                    values=["2", "3", "4", "6", "8"], width=5,
                    state="readonly").grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(self.custom_frame, text="Group:").grid(row=0, column=2, sticky=E, padx=(0, 5))
        ttk.Combobox(self.custom_frame, textvariable=self.q_group,
                    values=["32", "64", "128"], width=7,
                    state="readonly").grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(self.custom_frame, text="DType:").grid(row=0, column=4, sticky=E, padx=(0, 5))
        ttk.Combobox(self.custom_frame, textvariable=self.dtype,
                    values=["float16", "bfloat16", "float32"], width=10,
                    state="readonly").grid(row=0, column=5)
        
    def _build_advanced_section(self, parent):
        """Build collapsible advanced settings."""
        # Toggle button
        self.advanced_toggle = ttk.Checkbutton(parent, text="▶ Show Advanced Settings",
                                               variable=self.show_advanced,
                                               command=self._toggle_advanced)
        self.advanced_toggle.pack(anchor=W, pady=(0, 5))
        
        # Advanced frame (hidden by default)
        self.advanced_frame = ttk.LabelFrame(parent, text="Advanced Settings", padding="10")
        
        # Options
        ttk.Checkbutton(self.advanced_frame, text="Trust Remote Code",
                       variable=self.trust_remote).grid(row=0, column=0, sticky=W)
        
        ttk.Checkbutton(self.advanced_frame, text="HuggingFace Offline Mode",
                       variable=self.hf_offline).grid(row=0, column=1, sticky=W)
        
        ttk.Checkbutton(self.advanced_frame, text="Dry Run (preview only)",
                       variable=self.dry_run).grid(row=0, column=2, sticky=W)
        
        # Wired memory for Apple Silicon
        if platform.system() == "Darwin":
            mem_frame = ttk.Frame(self.advanced_frame)
            mem_frame.grid(row=1, column=0, columnspan=3, sticky=W, pady=(10, 0))
            
            ttk.Label(mem_frame, text="Apple Silicon Wired Memory (MB):").pack(side=LEFT, padx=(0, 5))
            ttk.Entry(mem_frame, textvariable=self.wired_memory, width=10).pack(side=LEFT, padx=(0, 5))
            ttk.Button(mem_frame, text="Copy sysctl Command",
                      command=self._copy_sysctl).pack(side=LEFT)
        
    def _build_log_section(self, parent):
        """Build the log output section."""
        frame = ttk.LabelFrame(parent, text="Conversion Log", padding="5")
        frame.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        # Scrolled text widget
        self.log_text = ScrolledText(frame, height=12, wrap='word')
        self.log_text.pack(fill=BOTH, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(frame, mode='indeterminate')
        self.progress.pack(fill=X, pady=(5, 0))
        
    def _build_action_buttons(self, parent):
        """Build the main action buttons at the bottom."""
        frame = ttk.Frame(parent)
        frame.pack(fill=X)
        
        # Left side - utility buttons
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=LEFT)
        
        ttk.Button(left_frame, text="Preview Command",
                  command=self._preview_command).pack(side=LEFT, padx=(0, 5))
        
        ttk.Button(left_frame, text="Clear Log",
                  command=self._clear_log).pack(side=LEFT)
        
        # Right side - main action button (prominent)
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=RIGHT)
        
        self.stop_btn = ttk.Button(right_frame, text="Stop",
                                  command=self._stop_conversion,
                                  state=DISABLED)
        self.stop_btn.pack(side=LEFT, padx=(0, 5))
        
        # Main conversion button - styled to be prominent
        self.convert_btn = ttk.Button(right_frame, text="Convert Model",
                                     command=self._run_conversion)
        self.convert_btn.pack(side=LEFT)
        self.convert_btn.configure(style='Accent.TButton')
        
        # Style the accent button
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Helvetica', 12, 'bold'))
        
    # UI Event Handlers
    
    def _browse_source(self):
        """Browse for source model."""
        # Try directory first
        path = filedialog.askdirectory(title="Select Model Directory")
        if not path:
            # Try file
            path = filedialog.askopenfilename(
                title="Select Model File",
                filetypes=[("Model Files", "*.safetensors *.nemo"), 
                          ("All Files", "*.*")])
        
        if path:
            self.source_path.set(path)
            
    def _browse_output(self):
        """Browse for output directory."""
        path = filedialog.askdirectory(title="Select Output Base Directory")
        if path:
            self.output_base.set(path)
            
    def _open_output(self):
        """Open output directory in file explorer."""
        path = self.output_base.get()
        if os.path.exists(path):
            if platform.system() == "Darwin":
                subprocess.call(["open", path])
            elif platform.system() == "Windows":
                os.startfile(path)
            else:
                subprocess.call(["xdg-open", path])
        else:
            messagebox.showwarning("Directory Not Found", 
                                  f"Directory does not exist: {path}")
            
    def _on_preset_change(self, event=None):
        """Handle preset selection change."""
        preset = self.preset.get()
        if preset == "Custom":
            self.custom_frame.pack(fill=X, pady=(5, 0))
        else:
            self.custom_frame.pack_forget()
            # Apply preset values
            if preset in PRESET_CONFIGS:
                bits, group, dtype = PRESET_CONFIGS[preset]
                if bits:
                    self.q_bits.set(bits)
                    self.q_group.set(group)
                    self.dtype.set(dtype)
                    
    def _toggle_advanced(self):
        """Toggle advanced settings visibility."""
        if self.show_advanced.get():
            self.advanced_frame.pack(fill=X, pady=(0, 10), before=self.log_text.master)
            self.advanced_toggle.configure(text="▼ Hide Advanced Settings")
        else:
            self.advanced_frame.pack_forget()
            self.advanced_toggle.configure(text="▶ Show Advanced Settings")
            
    def _update_ui_state(self):
        """Update UI element states based on settings."""
        if self.enable_quant.get():
            self.preset_combo.configure(state="readonly")
        else:
            self.preset_combo.configure(state=DISABLED)
            self.custom_frame.pack_forget()
            
    def _copy_sysctl(self):
        """Copy sysctl command to clipboard."""
        cmd = f"sudo sysctl iogpu.wired_limit_mb={self.wired_memory.get()}"
        self.clipboard_clear()
        self.clipboard_append(cmd)
        self._log(f"Copied to clipboard: {cmd}")
        
    def _clear_log(self):
        """Clear the log."""
        self.log_text.delete("1.0", END)
        
    def _log(self, message, level="INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(END, f"[{timestamp}] {level}: {message}\n")
        self.log_text.see(END)
        self.update_idletasks()
        
    # Conversion Logic
    
    def _detect_source_type(self, path):
        """Detect the type of source."""
        path = path.strip()
        
        # Check if it's a HuggingFace repo ID
        if "/" in path and not os.path.exists(path):
            return "hf"
        
        # Check if it's a local path
        if os.path.exists(path):
            if os.path.isdir(path):
                return "local"
            elif path.endswith(('.safetensors', '.nemo')):
                return "file"
                
        # Default to HF if uncertain
        return "hf"
        
    def _generate_output_path(self, source_path, source_type):
        """Generate a unique output path."""
        base = self.output_base.get()
        
        # Extract model name
        if source_type == "hf":
            model_name = source_path.replace("/", "_")
        elif source_type == "file":
            model_name = Path(source_path).stem
        else:
            model_name = Path(source_path).name
            
        # Add timestamp if enabled
        if self.auto_timestamp.get():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name = f"{model_name}_{timestamp}"
            
        output_path = os.path.join(base, model_name)
        
        # Ensure uniqueness
        counter = 1
        original_path = output_path
        while os.path.exists(output_path):
            output_path = f"{original_path}_v{counter}"
            counter += 1
            
        return output_path
        
    def _build_command(self, source_path, output_path, source_type):
        """Build the conversion command."""
        # Use the new command format for Python 3.13+
        cmd = [sys.executable, "-m", "mlx_lm", "convert"]
        
        # Add source
        if source_type == "file" and source_path.endswith('.safetensors'):
            # For safetensors, use parent directory
            source_path = str(Path(source_path).parent)
            
        cmd.extend(["--hf-path", source_path])
        cmd.extend(["--mlx-path", output_path])
        
        # Add dtype
        cmd.extend(["--dtype", self.dtype.get()])
        
        # Add quantization if enabled
        if self.enable_quant.get():
            cmd.append("-q")
            cmd.extend(["--q-bits", self.q_bits.get()])
            cmd.extend(["--q-group-size", self.q_group.get()])
            
        # Add optional flags
        if self.trust_remote.get():
            cmd.append("--trust-remote-code")
            
        return cmd
        
    def _preview_command(self):
        """Preview the command that will be run."""
        source = self.source_path.get().strip()
        if not source:
            messagebox.showwarning("No Source", "Please specify a model source.")
            return
            
        source_type = self._detect_source_type(source)
        output_path = self._generate_output_path(source, source_type)
        
        # Handle .nemo files
        if source.endswith('.nemo'):
            self._log("=" * 80)
            self._log("NeMo files require separate conversion to HuggingFace format first.")
            self._log("Install nemo2hf: pip install nemo2hf")
            self._log("Then run: python -m nemo2hf --in input.nemo --out temp_dir")
            self._log("Finally, use this tool on the temp_dir")
            self._log("=" * 80)
            return
            
        cmd = self._build_command(source, output_path, source_type)
        
        self._log("=" * 80)
        self._log("COMMAND PREVIEW")
        self._log(f"Source Type: {source_type.upper()}")
        self._log(f"Output Path: {output_path}")
        self._log("Command:")
        self._log("  " + " ".join(shlex.quote(arg) for arg in cmd))
        self._log("=" * 80)
        
    def _run_conversion(self):
        """Run the actual conversion."""
        # Check if already running
        if self.worker_thread and self.worker_thread.is_alive():
            messagebox.showwarning("Already Running", 
                                  "A conversion is already in progress.")
            return
            
        # Validate input
        source = self.source_path.get().strip()
        if not source:
            messagebox.showwarning("No Source", "Please specify a model source.")
            return
            
        # Check for .nemo files
        if source.endswith('.nemo'):
            messagebox.showinfo("NeMo Files", 
                              "NeMo files must be converted to HuggingFace format first.\n"
                              "See the log for instructions.")
            self._preview_command()
            return
            
        # Detect source type
        source_type = self._detect_source_type(source)
        
        # Generate output path
        output_path = self._generate_output_path(source, source_type)
        
        # Ensure base directory exists (but NOT the final output path - mlx_lm creates that)
        base_dir = self.output_base.get()
        try:
            os.makedirs(base_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Base Directory Error", f"Could not create base directory: {e}")
            return
            
        # Build command
        cmd = self._build_command(source, output_path, source_type)
        
        # Log start
        self._log("=" * 80)
        self._log(f"Starting conversion: {source} -> {output_path}")
        self._log("Command: " + " ".join(shlex.quote(arg) for arg in cmd))
        
        if self.dry_run.get():
            self._log("DRY RUN - Not executing command")
            self._log("=" * 80)
            return
            
        # Update UI
        self.convert_btn.configure(state=DISABLED)
        self.stop_btn.configure(state=NORMAL)
        self.progress.start(10)
        
        # Setup environment
        env = os.environ.copy()
        if self.hf_offline.get():
            env["HF_HUB_OFFLINE"] = "1"
            
        # Run in thread
        def worker():
            try:
                self.current_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    env=env
                )
                
                # Stream output
                for line in self.current_process.stdout:
                    self._log(line.rstrip())
                    
                return_code = self.current_process.wait()
                
                if return_code == 0:
                    self._log("SUCCESS: Conversion completed!", "SUCCESS")
                    self._log(f"Output saved to: {output_path}")
                else:
                    self._log(f"ERROR: Conversion failed (exit code {return_code})", "ERROR")
                    
            except Exception as e:
                self._log(f"ERROR: {e}", "ERROR")
            finally:
                # Reset UI
                self.progress.stop()
                self.convert_btn.configure(state=NORMAL)
                self.stop_btn.configure(state=DISABLED)
                self.current_process = None
                self._log("=" * 80)
                
        self.worker_thread = threading.Thread(target=worker, daemon=True)
        self.worker_thread.start()
        
    def _stop_conversion(self):
        """Stop the current conversion."""
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()
            self._log("Stopping conversion...", "WARNING")
            

def main():
    """Main entry point."""
    app = MLXQuantizeApp()
    app.mainloop()
    

if __name__ == "__main__":
    main()
