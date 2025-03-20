RESOLUME COMPOSITION CONVERTER - SOURCE PACKAGE

This folder contains everything needed to compile the Resolume Composition Converter application for Windows and macOS.

## Repository Structure

- `/` - Core application files
- `/build/mac/` - Mac-specific build files
- `/build/windows/` - Windows-specific build files
- `/dist/mac/` - Output directory for Mac builds
- `/dist/windows/` - Output directory for Windows builds
- `/screenshots/` - Application screenshots

## Building for macOS

1. Make sure you have Python 3.8 or newer installed
2. Open a terminal in this folder
3. Run the following commands:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pyinstaller build/mac/resolume_converter.spec
   python convert_manual_simple.py
   python create_distribution.py
   ```

## Building for Windows

1. Make sure you have Python 3.8 or newer installed
2. Open a command prompt in this folder
3. Run the following commands:
   ```
   python -m venv venv
   venv\Scripts\activate
   cd build/windows
   python build_windows.py
   ```

For detailed Windows build instructions, please refer to the `build/windows/PC_BUILD_INSTRUCTIONS.md` file.

## Core Files

- resolume_gui.py - Main application code
- runtime_hook.py - Runtime hook for PyInstaller to fix library loading issues
- convert_manual_simple.py - Script to create HTML documentation
- create_distribution.py - Script to create distribution package
- requirements.txt - Python dependencies
- README.md - Application overview
- MANUAL.md - User manual (Markdown format)
- LICENSE - MIT License
- SECURITY.md - Security policy
- CODE_OF_CONDUCT.md - Code of conduct
- CONTRIBUTING.md - Contributing guidelines

## Mac-Specific Files

- build/mac/resolume_converter.spec - PyInstaller specification file for macOS

## Windows-Specific Files

- build/windows/resolume_converter_windows.spec - PyInstaller specification file for Windows
- build/windows/PC_BUILD_INSTRUCTIONS.md - Detailed Windows build instructions
- build/windows/create_windows_icon.py - Script to create Windows icon (.ico) file
- build/windows/build_windows.py - Script to build the application on Windows
