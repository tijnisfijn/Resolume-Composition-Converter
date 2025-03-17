# Resolume Composition Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos)

A desktop application for converting Resolume Arena composition files (.avc) between different resolutions and frame rates. Automatically adjusts all parameters while preserving timing and composition names.

![Resolume Composition Converter](screenshots/app_screenshot.png)

## Features

- Convert Resolume Arena compositions between different resolutions
- Adjust frame rates while preserving timing
- Maintain composition names and structure
- Support for various media types (videos and images)
- Preserve aspect ratio for different image formats (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp)
- Simple and intuitive user interface

## Repository Structure

- `/` - Core application files
- `/build/mac/` - Mac-specific build files
- `/build/windows/` - Windows-specific build files
- `/dist/mac/` - Output directory for Mac builds
- `/dist/windows/` - Output directory for Windows builds
- `/screenshots/` - Application screenshots
- `/icons/` - Application icons
- `/documentation/` - Generated documentation

## Installation

### macOS

1. Download the latest release from the [Releases page](https://github.com/tijnisfijn/Resolume-Composition-Converter/releases)
2. Extract the ZIP file
3. Drag the `Resolume Composition Converter.app` to your Applications folder

### Windows

Windows users need to build the application from source:

1. Download the source code from the [Releases page](https://github.com/tijnisfijn/Resolume-Composition-Converter/releases)
2. Follow the instructions in `build/windows/PC_BUILD_INSTRUCTIONS.md`

## Usage

1. Launch the application
2. Select your input composition file (.avc)
3. Choose an output location for the converted file
4. Set your desired resolution and frame rate
5. Click "Convert Composition"

For more detailed instructions, please refer to the [User Manual](MANUAL.md).

## Building from Source

### Prerequisites

- Python 3.8 or newer
- pip (Python package installer)

### macOS

```bash
# Clone the repository
git clone https://github.com/tijnisfijn/Resolume-Composition-Converter.git
cd Resolume-Composition-Converter

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build the application
python build/mac/build_mac.py
```

### Windows

```bash
# Clone the repository
git clone https://github.com/tijnisfijn/Resolume-Composition-Converter.git
cd Resolume-Composition-Converter

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build the application
python build/windows/build_windows.py
```

## Support

For help and support, please [open an issue](https://github.com/tijnisfijn/Resolume-Composition-Converter/issues) on our GitHub repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.