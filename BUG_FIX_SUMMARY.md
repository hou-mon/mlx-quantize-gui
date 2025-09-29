# Critical Bug Fix - v2.0.1

## The Problem

Your conversion was failing with this error:
```
ValueError: Cannot save to the path /Users/Shared/moondream3-preview_20250929_185209 
as it already exists. Please delete the file/directory or specify a new path to save to.
```

## Root Cause

The bug was on **line 535** of `mlx_quantize_gui_v2.py`:

```python
# Create output directory
os.makedirs(output_path, exist_ok=True)
```

The code was pre-creating the timestamped output directory before calling mlx_lm. However, mlx_lm's convert command **expects to create that directory itself** and throws an error if it already exists.

So the sequence was:
1. Your code creates: `/Users/Shared/moondream3-preview_20250929_185209`
2. mlx_lm tries to create the same directory
3. mlx_lm fails because directory already exists

## The Fix

Changed the code to only ensure the **base** directory exists, not the final timestamped folder:

```python
# Ensure base directory exists (but NOT the final output path - mlx_lm creates that)
base_dir = self.output_base.get()
os.makedirs(base_dir, exist_ok=True)
```

Now the sequence is:
1. Your code ensures: `/Users/Shared` exists
2. mlx_lm creates: `/Users/Shared/moondream3-preview_20250929_185209`
3. Success

## Files Updated

1. **mlx_quantize_gui_v2.py** - Fixed the directory creation logic
2. **CHANGELOG_v2.md** - Documented the fix as version 2.0.1

## Testing

Try running your conversion again. It should work now. The error was preventing ALL conversions from succeeding, so this fix is critical.

## Why This Happened

This is a common integration issue - the GUI tool was being helpful by creating directories, but mlx_lm has its own directory creation logic and validation. The two systems conflicted.

## Ready for Open Source

With this fix, the tool should work reliably. All conversions should now complete successfully.
