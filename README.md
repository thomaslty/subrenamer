# SubRenamer

A macOS application for automatically renaming subtitle files to match video files through drag & drop.

## Features

- **Drag & Drop Interface**: Simply drag video and subtitle files into the application
- **Smart Matching**: Automatically matches subtitle files with video files based on filename similarity
- **Three-Column View**: Shows video files, original subtitle names, and proposed new names
- **Resizable Columns**: Adjust column widths to see full filenames
- **In-Place Renaming**: Renames subtitle files directly in their original location
- **macOS Native**: Built specifically for macOS with native .dmg packaging

## Supported File Types

### Video Files
- MP4, AVI, MKV, MOV, WMV, FLV, WebM
- M4V, MPG, MPEG, 3GP, TS, MTS

### Subtitle Files
- SRT, ASS, SSA, SUB, VTT, SBV, DFXP

## Installation

1. Download the latest `SubRenamer-x.x.x.dmg` from releases
2. Open the DMG file
3. Drag SubRenamer to your Applications folder

## Development

### Prerequisites

- Python 3.8+
- macOS 10.15+

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd subrenamer
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

### Building

To build the macOS app bundle and DMG:

```bash
./build.sh
```

This will create:
- `dist/SubRenamer.app` - The application bundle
- `SubRenamer-1.0.0.dmg` - The installer DMG

## Usage

1. Launch SubRenamer
2. Drag video files and subtitle files into the application window
3. Review the automatic matching in the three columns:
   - **Video File**: Your video filename
   - **Original Subtitle**: Current subtitle filename
   - **Renamed Subtitle**: Proposed new subtitle filename
4. Click **Submit** to rename the subtitle files
5. Use **Clear List** to remove all files and start over

## How It Works

SubRenamer uses intelligent filename matching to pair video and subtitle files:

1. **Normalization**: Removes common tags, separators, and formatting
2. **Similarity Scoring**: Uses sequence matching to find the best pairs
3. **Directory Preference**: Gives bonus points for files in the same folder
4. **Safe Renaming**: Checks for conflicts before renaming

## License

This project is open source. Feel free to use and modify as needed.