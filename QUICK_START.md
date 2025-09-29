# Quick Start Guide

## Installation

```bash
pip install -U mlx-lm
python3 mlx_quantize_gui_v2.py
```

## Simple 3-Step Process

### Step 1: Select Model Source
Enter one of:
- Local path: `/path/to/your/model`
- HuggingFace ID: `meta-llama/Llama-3.2-3B`
- Model file: `/path/to/model.safetensors`

### Step 2: Configure Output
- Default: `~/MLX_Models`
- Auto-timestamp enabled (prevents conflicts)
- Each conversion creates a unique folder

### Step 3: Convert
- Choose a preset or use default "Fast & Good (4-bit)"
- Click "Convert Model" button at bottom
- Watch the log for progress

## That's it!

The tool handles all the complexity for you:
- Detects source type automatically
- Prevents output conflicts with timestamps
- Uses optimal settings by default
- Shows clear error messages if something goes wrong

## Common Tasks

### Quick 4-bit Conversion
1. Paste your model path
2. Click "Convert Model"
3. Done

### Custom Settings
1. Select "Custom" preset
2. Adjust bits, group size, dtype
3. Click "Convert Model"

### Preview First
- Click "Preview Command" to see what will run
- Enable "Dry Run" in Advanced Settings for testing

## If Something Goes Wrong

1. Check the log for specific errors
2. Verify model path exists
3. Ensure mlx-lm is installed: `pip show mlx-lm`
4. Make sure you have disk space

## Tips

- **Use default settings** - They work well for most models
- **Keep timestamps on** - Prevents overwrites and conflicts
- **Watch the log** - Shows real-time conversion progress
- **Preview first** - Use "Preview Command" to verify settings

## Need More Control?

Click "Show Advanced Settings" for:
- Trust remote code toggle
- Offline mode for HuggingFace
- Dry run mode
- Apple Silicon memory settings

## Performance Boost (Apple Silicon)

For faster conversions on M-series Macs:

```bash
# Copy command from Advanced Settings, or use:
sudo sysctl iogpu.wired_limit_mb=96000  # For 128GB RAM
```

Adjust based on your RAM. Resets on reboot.
