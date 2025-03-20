# Building from Source

This page provides detailed instructions for building the Resolume Composition Converter from source code on different platforms.

## Prerequisites

- Python 3.8 or newer
- pip (Python package installer)
- Git (for cloning the repository)

## Repository Structure

The repository has the following structure:
- `/` - Core application files
- `/build/mac/` - Mac-specific build files
- `/build/windows/` - Windows-specific build files
- `/dist/mac/` - Output directory for Mac builds
- `/dist/windows/` - Output directory for Windows builds
- `/screenshots/` - Application screenshots
- `/icons/` - Application icons
- `/documentation/` - Generated documentation

## Building for macOS

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tijnisfijn/Resolume-Composition-Converter.git
   cd Resolume-Composition-Converter
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Build the application**:
   ```bash
   python build/mac/build_mac.py
   ```

5. **Find the built application**:
   The application will be in the `dist/mac/` directory.

## Building for Windows

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tijnisfijn/Resolume-Composition-Converter.git
   cd Resolume-Composition-Converter
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install Pillow
   ```

4. **Build the application**:
   ```bash
   python build/windows/build_windows.py
   ```

5. **Find the built application**:
   The application will be in the `dist/windows/` directory.

## Troubleshooting Windows Build

### Common Issues

1. **"Spec file not found" error**:
   - Make sure you're in the root directory of the repository
   - Verify that the file `build/windows/resolume_converter_windows.spec` exists

2. **"No module named 'PIL'" error**:
   - Make sure you've installed Pillow: `pip install Pillow`

3. **"No module named 'PyInstaller'" error**:
   - Make sure you've installed the requirements: `pip install -r requirements.txt`

4. **Icon creation fails**:
   - Verify that the `icons/app_icon.png` file exists
   - Make sure Pillow is installed: `pip install Pillow`

### Checking File Structure

If you're having issues, verify that your directory structure looks like this:
```
Resolume-Composition-Converter/
├── build/
│   ├── mac/
│   │   ├── build_mac.py
│   │   └── resolume_converter.spec
│   └── windows/
│       ├── build_windows.py
│       ├── create_windows_icon.py
│       ├── PC_BUILD_INSTRUCTIONS.md
│       └── resolume_converter_windows.spec
├── dist/
│   ├── mac/
│   └── windows/
├── screenshots/
├── resolume_gui.py
├── runtime_hook.py
├── convert_manual_simple.py
├── create_distribution.py
├── requirements.txt
└── other files...
```

## What the Build Scripts Do

### Mac Build Script (`build/mac/build_mac.py`)

The build script will:
1. Install the required dependencies
2. Build the application using PyInstaller with the correct spec file
3. Create HTML documentation
4. Create a distribution package
5. Move the built application to the dist/mac directory

### Windows Build Script (`build/windows/build_windows.py`)

The build script will:
1. Install the required dependencies
2. Install Pillow for icon creation
3. Create a Windows icon (.ico) file from the PNG icon
4. Build the application using PyInstaller with the correct spec file
5. Create HTML documentation
6. Create a distribution package
7. Move the built application to the dist/windows directory

## Creating a Source Package

If you want to create a source package for distribution:

```bash
python create_source_package.py
```

This will create a ZIP file containing all the necessary files to build the application on any platform.