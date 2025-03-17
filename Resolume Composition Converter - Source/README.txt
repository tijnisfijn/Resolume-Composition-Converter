RESOLUME COMPOSITION CONVERTER - SOURCE PACKAGE

This folder contains everything needed to compile the Resolume Composition Converter application for Windows and macOS.

To build the application:

1. Make sure you have Python 3.8 or newer installed
2. Open a command prompt in this folder
3. Follow the instructions in BUILD_INSTRUCTIONS.md

For detailed build instructions, please refer to the BUILD_INSTRUCTIONS.md file.

Files included:
- resolume_gui.py - Main application code
- resolume_converter.spec - PyInstaller specification file for macOS
- resolume_converter_windows.spec - PyInstaller specification file for Windows
- runtime_hook.py - Runtime hook for PyInstaller to fix library loading issues
- convert_manual_simple.py - Script to create HTML documentation
- create_distribution.py - Script to create distribution package
- build_windows.py - Script to build the application on Windows
- create_windows_icon.py - Script to create Windows icon (.ico) file
- requirements.txt - Python dependencies
- BUILD_INSTRUCTIONS.md - Detailed build instructions
- README.md - Application overview
- MANUAL.md - User manual (Markdown format)
- LICENSE - MIT License
- screenshots/ - Application screenshots

Windows-specific files:
- resolume_converter_windows.spec - Optimized spec file for Windows builds
- build_windows.py - Script to build the application on Windows
- create_windows_icon.py - Script to create Windows icon (.ico) file

macOS-specific files:
- resolume_converter.spec - Optimized spec file for macOS builds
