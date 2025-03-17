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

def create_windows_build_instructions():
    """Create a BUILD_INSTRUCTIONS.md file with Windows build instructions"""
    print("Creating Windows build instructions...")
    
    instructions = """# Build Instructions for Windows

## Prerequisites

1. **Python 3.8 or newer**
   - Download and install from [python.org](https://www.python.org/downloads/windows/)
   - Make sure to check "Add Python to PATH" during installation

2. **Git** (optional, for version control)
   - Download and install from [git-scm.com](https://git-scm.com/download/win)

## Setup

1. **Create a virtual environment**:
   ```
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   ```
   venv\\Scripts\\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Building the Application

1. **Run the build script**:
   ```
   python build_windows.py
   ```

   This will:
   - Build the application using PyInstaller
   - Create the HTML documentation
   - Package everything into a distribution folder

2. **Alternative manual build**:
   ```
   pyinstaller resolume_converter.spec
   python convert_manual_simple.py
   python create_distribution.py
   ```

## Output

After building, you'll find:

1. **dist/Resolume Composition Converter.exe** - The executable application
2. **Resolume Composition Converter/** - A folder containing the application and documentation
3. **Resolume Composition Converter.zip** - A ZIP archive of the folder

## Troubleshooting

- If you encounter issues with tkinter, make sure you have the tk package installed:
  ```
  pip install tk
  ```

- If PyInstaller fails, try running:
  ```
  pip uninstall pyinstaller
  pip install pyinstaller
  ```

- For any other issues, please refer to the PyInstaller documentation:
  [PyInstaller Windows Documentation](https://pyinstaller.org/en/stable/usage.html#windows)
"""
    
    with open("BUILD_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print("BUILD_INSTRUCTIONS.md created successfully")
    return True

def create_windows_build_script():
    """Create a build_windows.py script for Windows"""
    print("Creating Windows build script...")
    
    script = """#!/usr/bin/env python3
\"\"\"
Build script for Windows
\"\"\"

import os
import sys
import subprocess
import shutil

def main():
    \"\"\"Main function\"\"\"
    print("Building Resolume Composition Converter for Windows...")
    
    # Activate virtual environment if not already activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Virtual environment not activated. It's recommended to run this script in a virtual environment.")
    
    # Install requirements
    print("\\nInstalling requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Build the application
    print("\\nBuilding application with PyInstaller...")
    subprocess.run([sys.executable, "-m", "PyInstaller", "resolume_converter.spec"], check=True)
    
    # Create HTML documentation
    print("\\nCreating HTML documentation...")
    subprocess.run([sys.executable, "convert_manual_simple.py"], check=True)
    
    # Create distribution package
    print("\\nCreating distribution package...")
    subprocess.run([sys.executable, "create_distribution.py"], check=True)
    
    print("\\nBuild completed successfully!")
    print("You can find the application in the 'Resolume Composition Converter' folder")
    print("or in the 'Resolume Composition Converter.zip' archive.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
    
    with open("build_windows.py", "w") as f:
        f.write(script)
    
    print("build_windows.py created successfully")
    return True

def create_source_package():
    """Create a source package with everything needed to compile the application"""
    print("Creating source package...")
    
    # Create source package folder
    source_folder = "Resolume Composition Converter - Source"
    if os.path.exists(source_folder):
        print(f"Removing existing source folder: {source_folder}")
        shutil.rmtree(source_folder)
    
    os.makedirs(source_folder, exist_ok=True)
    
    # Create requirements.txt
    create_requirements_file()
    
    # Create Windows build instructions
    create_windows_build_instructions()
    
    # Create Windows build script
    create_windows_build_script()
    
    # Files to copy
    files_to_copy = [
        "resolume_gui.py",
        "resolume_converter.spec",
        "resolume_converter_windows.spec",
        "runtime_hook.py",
        "convert_manual_simple.py",
        "create_distribution.py",
        "build_windows.py",
        "requirements.txt",
        "BUILD_INSTRUCTIONS.md",
        "README.md",
        "LICENSE",
        "MANUAL.md"
    ]
    
    # Copy files
    print("Copying files...")
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, f"{source_folder}/{file}")
            print(f"Copied {file}")
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
- requirements.txt - Python dependencies
- BUILD_INSTRUCTIONS.md - Detailed build instructions
- README.md - Application overview
- MANUAL.md - User manual (Markdown format)
- LICENSE - MIT License
- screenshots/ - Application screenshots

Windows-specific files:
- resolume_converter_windows.spec - Optimized spec file for Windows builds
- build_windows.py - Script to build the application on Windows

macOS-specific files:
- resolume_converter.spec - Optimized spec file for macOS builds
"""
    
    with open(f"{source_folder}/README.txt", "w") as f:
        f.write(readme_txt)
    
    print("Created README.txt with instructions")
    
    # Create ZIP archive
    print("\nCreating ZIP archive...")
    try:
        shutil.make_archive(source_folder, 'zip', '.', source_folder)
        print(f"ZIP archive created: {source_folder}.zip")
    except Exception as e:
        print(f"Error creating ZIP archive: {e}")
    
    print(f"\nSource package created successfully: {source_folder}")
    print(f"ZIP archive: {source_folder}.zip")
    
    return True

def main():
    """Main function"""
    create_source_package()
    
    print("\nSource package created successfully!")
    print("You can now share the source package with your friend to build the application on Windows.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())