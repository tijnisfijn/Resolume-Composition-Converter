#!/usr/bin/env python3
"""
Script to create a source package with everything needed to compile the application
"""

import os
import sys
import shutil
import subprocess

def create_requirements_file():
    """Create a requirements.txt file with all dependencies"""
    print("Creating requirements.txt file...")
    try:
        # Use pip freeze to get all installed packages
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Filter out packages that are not needed
        requirements = []
        for line in result.stdout.splitlines():
            # Include only the packages we need
            if any(pkg in line.lower() for pkg in ["pyinstaller", "markdown", "tkinter"]):
                requirements.append(line)
        
        # Add specific versions we know work
        requirements.extend([
            "pyinstaller>=6.0.0",
            "markdown>=3.0.0"
        ])
        
        # Remove duplicates
        requirements = list(set(requirements))
        
        # Write to requirements.txt
        with open("requirements.txt", "w") as f:
            f.write("\n".join(requirements))
        
        print("requirements.txt created successfully")
        return True
    except Exception as e:
        print(f"Error creating requirements.txt: {e}")
        # Create a basic requirements file as fallback
        with open("requirements.txt", "w") as f:
            f.write("pyinstaller>=6.0.0\nmarkdown>=3.0.0\n")
        print("Created basic requirements.txt as fallback")
        return True

def create_source_package():
    """Create a source package with everything needed to compile the application"""
    print("Creating source package...")
    
    # Create source package folder
    source_folder = "Resolume-Composition-Converter-Source"
    if os.path.exists(source_folder):
        print(f"Removing existing source folder: {source_folder}")
        shutil.rmtree(source_folder)
    
    os.makedirs(source_folder, exist_ok=True)
    
    # Create platform-specific build directories
    os.makedirs(f"{source_folder}/build/mac", exist_ok=True)
    os.makedirs(f"{source_folder}/build/windows", exist_ok=True)
    os.makedirs(f"{source_folder}/dist/mac", exist_ok=True)
    os.makedirs(f"{source_folder}/dist/windows", exist_ok=True)
    
    # Create requirements.txt
    create_requirements_file()
    
    # Core files to copy to the root directory
    core_files = [
        "resolume_gui.py",
        "runtime_hook.py",
        "convert_manual_simple.py",
        "create_distribution.py",
        "requirements.txt",
        "README.md",
        "LICENSE",
        "MANUAL.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "GITHUB_DESCRIPTION.md"
    ]
    
    # Mac-specific files to copy
    mac_files = [
        "resolume_converter.spec"
    ]
    
    # Windows-specific files to copy
    windows_files = [
        "resolume_converter_windows.spec",
        "PC_BUILD_INSTRUCTIONS.md",
        "create_windows_icon.py",
        "build_windows.py"
    ]
    
    # Copy core files
    print("Copying core files...")
    for file in core_files:
        if os.path.exists(file):
            shutil.copy(file, f"{source_folder}/{file}")
            print(f"Copied {file}")
        else:
            print(f"Warning: {file} not found")
    
    # Copy Mac-specific files
    print("Copying Mac-specific files...")
    for file in mac_files:
        if os.path.exists(file):
            shutil.copy(file, f"{source_folder}/build/mac/{file}")
            print(f"Copied {file} to build/mac/")
        elif os.path.exists(f"build/mac/{file}"):
            shutil.copy(f"build/mac/{file}", f"{source_folder}/build/mac/{file}")
            print(f"Copied build/mac/{file} to source package")
        else:
            print(f"Warning: {file} not found")
    
    # Copy Windows-specific files
    print("Copying Windows-specific files...")
    for file in windows_files:
        if os.path.exists(file):
            shutil.copy(file, f"{source_folder}/build/windows/{file}")
            print(f"Copied {file} to build/windows/")
        elif os.path.exists(f"build/windows/{file}"):
            shutil.copy(f"build/windows/{file}", f"{source_folder}/build/windows/{file}")
            print(f"Copied build/windows/{file} to source package")
        else:
            print(f"Warning: {file} not found")
    
    # Copy screenshots folder
    if os.path.exists("screenshots"):
        shutil.copytree("screenshots", f"{source_folder}/screenshots")
        print("Copied screenshots folder")
    else:
        print("Warning: screenshots folder not found")
        os.makedirs(f"{source_folder}/screenshots", exist_ok=True)
    
    # Create a README.txt file with instructions
    readme_txt = """RESOLUME COMPOSITION CONVERTER - SOURCE PACKAGE

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
   venv\\Scripts\\activate
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
"""
    
    with open(f"{source_folder}/README.txt", "w") as f:
        f.write(readme_txt)
    
    print("Created README.txt with instructions")
    
    # Create ZIP archive
    print("\nCreating ZIP archive...")
    try:
        shutil.make_archive(f"Resolume-Composition-Converter-Source", 'zip', '.', source_folder)
        print(f"ZIP archive created: Resolume-Composition-Converter-Source.zip")
    except Exception as e:
        print(f"Error creating ZIP archive: {e}")
    
    print(f"\nSource package created successfully: {source_folder}")
    print(f"ZIP archive: Resolume-Composition-Converter-Source.zip")
    
    return True

def main():
    """Main function"""
    create_source_package()
    
    print("\nSource package created successfully!")
    print("You can now share the source package with others to build the application on Windows or macOS.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())