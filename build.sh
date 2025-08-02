#!/bin/bash

# Build script for SubRenamer macOS app

set -e

echo "Building SubRenamer for macOS..."

# Activate virtual environment
source .venv/bin/activate

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/

# Build the app bundle
echo "Building app bundle..."
python setup.py py2app

# Create DMG
echo "Creating DMG..."
dmgbuild -s dmg_settings.py "SubRenamer" "SubRenamer-1.0.0.dmg"

echo "Build complete! DMG created: SubRenamer-1.0.0.dmg"
echo "App bundle location: dist/SubRenamer.app"