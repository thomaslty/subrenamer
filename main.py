#!/usr/bin/env python3
"""
SubRenamer - A macOS application for renaming subtitle files to match video files
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import SubRenamerApp

def main():
    """Main entry point for the application."""
    app = SubRenamerApp()
    app.run()

if __name__ == "__main__":
    main()