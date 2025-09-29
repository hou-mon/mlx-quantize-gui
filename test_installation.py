#!/usr/bin/env python3
"""
MLX Installation Tester
Tests if mlx-lm is properly installed and working
"""

import sys
import subprocess
import platform
from pathlib import Path

def test_python_version():
    """Check Python version."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  WARNING: Python 3.8+ recommended")
        return False
    print("  OK: Python version compatible")
    return True

def test_mlx_import():
    """Test if mlx-lm can be imported."""
    try:
        import mlx_lm
        print(f"mlx-lm import: OK")
        print(f"  Version info available: {hasattr(mlx_lm, '__version__')}")
        return True
    except ImportError as e:
        print(f"mlx-lm import: FAILED")
        print(f"  Error: {e}")
        print(f"  Install with: pip install -U mlx-lm")
        return False

def test_mlx_command():
    """Test if mlx_lm command works."""
    commands_to_try = [
        [sys.executable, "-m", "mlx_lm", "--help"],  # New format
        [sys.executable, "-m", "mlx_lm.convert", "--help"],  # Old format
    ]
    
    for cmd in commands_to_try:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"mlx_lm command: OK")
                print(f"  Using format: {' '.join(cmd[:4])}")
                return True
        except Exception:
            continue
    
    print("mlx_lm command: FAILED")
    print("  Could not run mlx_lm commands")
    return False

def test_disk_space():
    """Check available disk space."""
    home = Path.home()
    try:
        import shutil
        total, used, free = shutil.disk_usage(home)
        free_gb = free / (1024**3)
        print(f"Disk space: {free_gb:.1f} GB free")
        if free_gb < 10:
            print("  WARNING: Low disk space for model conversion")
            return False
        print("  OK: Sufficient disk space")
        return True
    except Exception as e:
        print(f"Disk space check: FAILED ({e})")
        return False

def test_platform():
    """Check platform information."""
    print(f"Platform: {platform.system()} {platform.machine()}")
    if platform.system() == "Darwin" and "arm" in platform.machine().lower():
        print("  OK: Apple Silicon detected - optimal for MLX")
    elif platform.system() == "Darwin":
        print("  OK: macOS detected")
    else:
        print("  INFO: Non-macOS system - MLX may have limited features")
    return True

def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("MLX Quantize & Convert - Installation Test")
    print("=" * 60)
    
    results = []
    results.append(("Python Version", test_python_version()))
    print()
    results.append(("Platform", test_platform()))
    print()
    results.append(("MLX Import", test_mlx_import()))
    print()
    results.append(("MLX Command", test_mlx_command()))
    print()
    results.append(("Disk Space", test_disk_space()))
    print()
    
    print("=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("All tests passed! You're ready to use mlx_quantize_gui_v2.py")
    else:
        print("Some tests failed. Please fix the issues above before running the converter.")
        print("\nQuick fix:")
        print("  pip install -U mlx-lm")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
