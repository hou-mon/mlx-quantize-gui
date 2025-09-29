# MLX Quantize & Convert v2.0

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)
![MLX](https://img.shields.io/badge/MLX-compatible-orange)

A streamlined GUI application for converting and quantizing machine learning models to Apple's MLX format. Built with simplicity and reliability in mind.

## Features

- **Smart Source Detection**: Automatically detects local directories, HuggingFace repos, or single files
- **Automatic Conflict Resolution**: Timestamps prevent output directory conflicts
- **One-Click Conversion**: Prominent conversion button with clear workflow
- **Preset Configurations**: Quick settings for common use cases
- **Clean Interface**: Simplified 3-step process with optional advanced settings
- **Real-time Logging**: Monitor conversion progress with live output

## Requirements

```bash
pip install -U mlx-lm
```


## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -U mlx-lm
   ```

2. **Run the application:**
   ```bash
   python3 mlx_quantize_gui_v2.py
   ```

3. **Follow the 3-step process:**
   - Select your model (local path or HuggingFace ID)
   - Choose output directory (auto-timestamped to prevent conflicts)  
   - Configure quantization (or use a preset)
   - Click "Convert Model"

## Usage Examples

### Convert a HuggingFace Model
```
Model Path: meta-llama/Llama-3.2-3B
Output: ~/MLX_Models
Preset: Fast & Good (4-bit)
Creates: ~/MLX_Models/meta-llama_Llama-3.2-3B_20250101_120000
```

### Convert a Local Model
```
Model Path: /path/to/your/model
Output: ~/MLX_Models  
Preset: High Quality (8-bit)
Creates: ~/MLX_Models/model_20250101_120000
```

## Quantization Presets

| Preset | Bits | Group | DType | Use Case |
|--------|------|-------|-------|----------|
| **Fast & Good** | 4 | 64 | float16 | Best balance of speed and quality |
| **High Quality** | 8 | 64 | float16 | Maximum quality, larger size |
| **Tiny Size** | 2 | 128 | bfloat16 | Minimum size, lower quality |
| **Balanced** | 6 | 64 | float16 | Middle ground option |
| **Custom** | - | - | - | Manual configuration |

## Key Improvements in v2.0

### 1. Fixed Output Directory Conflicts
- Automatically adds timestamps to output folders
- Prevents "already exists" errors
- Optional timestamp toggle for advanced users

### 2. Simplified UI
- Clear 3-step workflow
- Conversion button prominently placed at bottom
- Advanced settings hidden by default
- Clean, uncluttered interface

### 3. Better Command Compatibility  
- Fixed Python 3.13 compatibility issues
- Uses new `mlx_lm convert` syntax
- Proper subprocess handling

### 4. Improved Error Handling
- Smart source type detection
- Clear error messages
- Validation before conversion starts
- Graceful failure recovery

## Advanced Settings

Click "Show Advanced Settings" to access:
- Trust remote code option
- HuggingFace offline mode  
- Dry run mode for testing
- Apple Silicon wired memory configuration

## Apple Silicon Performance

For better performance on M-series Macs, increase the integrated GPU wired memory:

```bash
sudo sysctl iogpu.wired_limit_mb=96000
```

Recommended values by RAM:
- 16GB RAM: 12000 (12GB)
- 32GB RAM: 24000 (24GB)
- 64GB RAM: 48000 (48GB)
- 128GB RAM: 96000 (96GB)
- 192GB RAM: 150000 (150GB)

Note: This setting is temporary and resets on reboot. Use with caution.

## Troubleshooting

### "Cannot save to path" Error
**Fixed in v2.0** - The tool now automatically adds timestamps to prevent conflicts.

### Command Compatibility Issues
**Fixed in v2.0** - Uses the new `mlx_lm convert` syntax for Python 3.13+.

### NeMo Files
NeMo files require conversion to HuggingFace format first:
```bash
pip install nemo2hf
python -m nemo2hf --in input.nemo --out temp_dir
```
Then use this tool on the temp_dir.

### Missing mlx-lm
Install or update:
```bash
pip install -U mlx-lm
```

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! This tool is designed to be simple, robust, and easy to maintain.

## Changelog

### v2.0 (2025)
- Complete UI redesign for simplicity
- Fixed output directory conflict issues
- Fixed Python 3.13 compatibility
- Added automatic timestamp feature
- Moved conversion button to prominent bottom position
- Simplified to 3-step workflow
- Added preset configurations
- Improved error handling and validation
- Removed complexity while maintaining configurability

### v1.0
- Initial release with full feature set
