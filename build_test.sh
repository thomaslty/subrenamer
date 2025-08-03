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
python setup.py py2app -A

# Test the alias build
echo "Testing the alias build..."
./dist/SubRenamer.app/Contents/MacOS/SubRenamer