#!/usr/bin/env python3
"""
Build script for Windows
"""

import os
import sys
import subprocess
import shutil

def main():
    """Main function"""
    print("Building Resolume Composition Converter for Windows...")
    
    # Get the repository root directory
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    # Change to the repository root directory
    os.chdir(repo_root)
    
    # Activate virtual environment if not already activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Virtual environment not activated. It's recommended to run this script in a virtual environment.")
    
    # Install requirements
    print("\nInstalling requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Install Pillow for icon creation
    print("\nInstalling Pillow for icon creation...")
    subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"], check=True)
    
    # Create Windows icon
    print("\nCreating Windows icon...")
    subprocess.run([sys.executable, "build/windows/create_windows_icon.py"], check=True)
    
    # Build the application
    print("\nBuilding application with PyInstaller...")
    subprocess.run([sys.executable, "-m", "PyInstaller", "build/windows/resolume_converter_windows.spec"], check=True)
    
    # Create HTML documentation
    print("\nCreating HTML documentation...")
    subprocess.run([sys.executable, "convert_manual_simple.py"], check=True)
    
    # Create distribution package
    print("\nCreating distribution package...")
    subprocess.run([sys.executable, "create_distribution.py"], check=True)
    
    # Move the built application to the dist/windows directory
    if os.path.exists("dist/Resolume Composition Converter"):
        if os.path.exists("dist/windows/Resolume Composition Converter"):
            shutil.rmtree("dist/windows/Resolume Composition Converter")
        shutil.move("dist/Resolume Composition Converter", "dist/windows/")
        print("\nMoved built application to dist/windows/")
    
    if os.path.exists("Resolume Composition Converter.zip"):
        if os.path.exists("dist/windows/Resolume Composition Converter.zip"):
            os.remove("dist/windows/Resolume Composition Converter.zip")
        shutil.move("Resolume Composition Converter.zip", "dist/windows/")
        print("Moved ZIP archive to dist/windows/")
    
    print("\nBuild completed successfully!")
    print("You can find the application in the 'dist/windows/Resolume Composition Converter' folder")
    print("or in the 'dist/windows/Resolume Composition Converter.zip' archive.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
