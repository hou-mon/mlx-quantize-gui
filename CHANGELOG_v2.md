# Changelog

## Version 2.0.1 (2025) - Critical Bug Fix

### Critical Fix
**Problem**: Directory pre-creation causing conversion failures  
**Root Cause**: Code was creating the output directory with `os.makedirs()` before running mlx_lm, but mlx_lm expects to create the directory itself and errors if it already exists  
**Solution**: Changed to only ensure the base directory exists, allowing mlx_lm to create the final timestamped folder  
**Impact**: This was preventing ALL conversions from completing successfully

## Version 2.0 (2025) - Complete Redesign

### Major Fixes

#### 1. Output Directory Conflict Resolution
**Problem**: MLX would fail with "Cannot save to path as it already exists" error
**Solution**: 
- Added automatic timestamp generation for output folders
- Each conversion creates a unique directory (e.g., `model_20250101_120000`)
- Optional toggle to disable timestamps for advanced users
- Automatic counter increment if timestamp directory somehow exists

#### 2. Python 3.13 Compatibility
**Problem**: Deprecated command format causing warnings and failures
**Solution**:
- Changed from `python -m mlx_lm.convert` to `python -m mlx_lm convert`
- Updated subprocess handling for better compatibility
- Fixed module import warnings

#### 3. UI/UX Overhaul
**Problem**: Conversion button buried in middle of interface, hard to find
**Solution**:
- Moved main "Convert Model" button to bottom-right (most prominent position)
- Styled as accent button with larger, bold font
- Clear visual hierarchy with numbered sections (1-2-3 workflow)
- Reduced visual clutter by hiding advanced options by default

### New Features

#### Simplified Workflow
- Reduced to 3 clear steps: Source → Output → Convert
- Smart source detection (auto-detects local vs HuggingFace)
- Single input field handles all source types
- Preset configurations for common use cases

#### Better Error Handling
- Validates paths before starting conversion
- Clear error messages in the log
- Graceful handling of missing directories
- Pre-conversion checks for common issues

#### Improved Logging
- Real-time output streaming
- Timestamp on every log entry
- Clear SUCCESS/ERROR/WARNING indicators
- Scrollable log with auto-scroll to bottom

### UI Improvements

#### Layout Changes
- Numbered sections for clear workflow
- Advanced settings in collapsible section
- Log takes up more space for better visibility
- Action buttons grouped logically at bottom

#### Simplified Options
- Presets replace complex configuration
- Custom settings only shown when needed
- Removed redundant options
- Cleaner labels and descriptions

### Code Quality

#### Architecture
- Cleaner separation of concerns
- Better method organization
- Improved variable naming
- More robust error handling

#### Maintenance
- Removed deprecated features
- Updated for latest mlx-lm syntax
- Better subprocess management
- Thread-safe operations

### Removed Complexity

#### Eliminated Features (for simplicity)
- Batch processing queue (rarely used, added complexity)
- NeMo bridge configuration (moved to documentation)
- Multiple source mode dropdowns (unified input field)
- Redundant configuration options
- Complex quantization predicates
- Upload to HuggingFace option
- Configuration save/load (settings are simple now)

#### Streamlined Settings
- Reduced from 20+ options to essential 6-8
- Presets cover 90% of use cases
- Advanced settings hidden by default
- Sensible defaults for everything

### Bug Fixes

- Fixed subprocess hanging on large outputs
- Fixed path normalization issues
- Fixed UI state management bugs
- Fixed progress bar not stopping
- Fixed button states during conversion
- Removed all emoji characters from codebase

### Platform Improvements

- Better cross-platform file explorer support
- Improved Windows compatibility
- Fixed macOS-specific issues
- Cleaner Linux support

### Documentation

- Simplified README
- Clearer quick start guide
- Removed outdated information
- Added troubleshooting for common issues
- Better examples and use cases

## Version 1.0 (Original)

- Initial release with full feature set
- Complex UI with many options
- Batch processing support
- NeMo file conversion
- Configuration management
- Multiple source modes
- HuggingFace upload integration

## Migration Guide (v1.0 → v2.0)

### What Changed

1. **Source Selection**: Instead of dropdown + multiple fields, use single input field
2. **Output Path**: Now auto-generates unique paths with timestamps
3. **Conversion Button**: Moved to bottom-right, clearly labeled
4. **Settings**: Most options now in presets or advanced section
5. **Batch Processing**: Removed - run multiple times for multiple models

### Why These Changes

- **Simplicity**: Reduced cognitive load for new users
- **Reliability**: Automatic conflict resolution prevents errors
- **Clarity**: Clear 3-step process anyone can follow
- **Maintainability**: Cleaner codebase easier to update

### For Power Users

Advanced features still available:
- Click "Show Advanced Settings" for fine control
- Use "Preview Command" to see exact command
- Disable timestamp for manual path control
- Custom preset allows full configuration
