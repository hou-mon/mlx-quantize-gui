#!/bin/bash

# Package MLX Quantize & Convert v2.0.1 (Fixed)

echo "Creating MLX Quantize & Convert v2.0.1 package..."

# Create directory
PACKAGE_NAME="mlx_quantize_v2.0.1"
mkdir -p "$PACKAGE_NAME"

# Copy files
cp mlx_quantize_gui_v2.py "$PACKAGE_NAME/"
cp README.md "$PACKAGE_NAME/"
cp QUICK_START.md "$PACKAGE_NAME/"
cp CHANGELOG_v2.md "$PACKAGE_NAME/CHANGELOG.md"
cp LICENSE "$PACKAGE_NAME/"
cp test_installation.py "$PACKAGE_NAME/"
cp BUG_FIX_SUMMARY.md "$PACKAGE_NAME/"

# Make scripts executable
chmod +x "$PACKAGE_NAME/mlx_quantize_gui_v2.py"
chmod +x "$PACKAGE_NAME/test_installation.py"

# Create zip archive
zip -r "${PACKAGE_NAME}.zip" "$PACKAGE_NAME"

echo "Package created: ${PACKAGE_NAME}.zip"
echo ""
echo "Contents:"
ls -la "$PACKAGE_NAME/"
echo ""
echo "To use:"
echo "  1. unzip ${PACKAGE_NAME}.zip"
echo "  2. cd ${PACKAGE_NAME}"
echo "  3. python3 test_installation.py  # Test setup"
echo "  4. python3 mlx_quantize_gui_v2.py  # Run converter"
