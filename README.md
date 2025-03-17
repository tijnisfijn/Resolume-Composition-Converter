# Resolume Composition Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)]()
[![Release](https://img.shields.io/github/v/release/yourusername/resolume-composition-converter?include_prereleases&sort=semver)](https://github.com/yourusername/resolume-composition-converter/releases)

A desktop application for converting Resolume Arena composition files (.avc) to different resolutions and frame rates.

![Resolume Composition Converter](./screenshots/app_screenshot.png)

## 🚀 Overview

Resolume Composition Converter allows you to easily convert your Resolume Arena compositions from one resolution and frame rate to another (e.g., from 1080p25 to 4K60). The application automatically adjusts all relevant parameters in the composition file, including:

- Composition resolution and name
- Layer and clip dimensions
- Transform effects (position, anchor points)
- Timeline durations
- File paths to media files

This tool is perfect for VJs, video artists, and Resolume users who need to adapt their compositions for different display setups or performance environments.

## ✨ Key Features

- Convert compositions between any resolution and frame rate
- Update file paths to media files in bulk
- Preserve custom durations and timing
- Automatically adjust transform effects
- Maintain composition names across conversions
- Simple, intuitive interface with dark mode
- Drag and drop support

## 📥 Installation

### Download Pre-built Application

#### macOS

1. Download the latest release from the [Releases](https://github.com/yourusername/resolume-composition-converter/releases) page
2. Unzip the file
3. Drag the `Resolume Composition Converter.app` to your Applications folder
4. Right-click the app and select "Open" (required only the first time you run the app)

#### Windows and Linux

Coming soon. In the meantime, you can build from source following the instructions below.

### Build from Source

#### Prerequisites

- Python 3.8 or newer
- Git (optional, for cloning the repository)

#### macOS

```bash
# Clone the repository
git clone https://github.com/yourusername/resolume-composition-converter.git
cd resolume-composition-converter

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build the application
pyinstaller resolume_converter.spec
python convert_manual_simple.py
python create_distribution.py
```

#### Windows

```bash
# Clone the repository
git clone https://github.com/yourusername/resolume-composition-converter.git
cd resolume-composition-converter

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build the application
python build_windows.py
```

## 📖 Quick Start Guide

1. Launch the application
2. Select your input composition file (.avc)
3. Choose an output location for the converted file
4. Optionally, update the file paths if your media files have moved
5. Set your desired resolution and frame rate
6. Click "Convert Composition"

## 🔧 Advanced Usage

### File Path Replacement

If you've moved your media files to a new location, you can use the "Old File Path" and "New File Path" fields to update all file references in the composition:

1. Enter the old path where your media files were located
2. Enter the new path where your media files are now
3. The converter will update all file references in the composition

### Custom Resolution and Frame Rate

You can set any custom resolution and frame rate:

1. Enter your original composition's resolution and frame rate in the "Original Settings" section
2. Enter your desired output resolution and frame rate in the "New Settings" section
3. The converter will calculate the appropriate scaling factors

## 🧩 How It Works

The converter works by:

1. Parsing the XML structure of the .avc file
2. Calculating scaling factors based on your desired resolution and frame rate
3. Adjusting all relevant parameters in the composition
4. Preserving custom durations and timing
5. Updating file paths if specified
6. Writing the modified XML to a new .avc file

## 💻 Development

### Project Structure

- `resolume_gui.py` - Main application code
- `convert_manual_simple.py` - Script to convert the manual to HTML
- `create_distribution.py` - Script to create the distribution package
- `build_windows.py` - Script to build the application for Windows

### Requirements

- Python 3.8 or newer
- Dependencies listed in `requirements.txt`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please make sure to update tests as appropriate and follow the code style of the project.

## 📋 Requirements

- macOS 10.14 or later (for the pre-built application)
- 64-bit processor
- Python 3.8 or newer (for building from source)

## 🐛 Known Issues

- Windows and Linux builds are still in development
- Some complex effects may require manual adjustment after conversion

## 📝 License

This software is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Support

For help and support, please [open an issue](https://github.com/yourusername/resolume-composition-converter/issues) on our GitHub repository.

## 🙏 Acknowledgements

- [Resolume](https://resolume.com/) for creating an amazing VJ software
- All contributors and testers who have helped improve this tool