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
    
    # Activate virtual environment if not already activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Virtual environment not activated. It's recommended to run this script in a virtual environment.")
    
    # Install requirements
    print("\nInstalling requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Build the application
    print("\nBuilding application with PyInstaller...")
    subprocess.run([sys.executable, "-m", "PyInstaller", "resolume_converter_windows.spec"], check=True)
    
    # Create HTML documentation
    print("\nCreating HTML documentation...")
    subprocess.run([sys.executable, "convert_manual_simple.py"], check=True)
    
    # Create distribution package
    print("\nCreating distribution package...")
    subprocess.run([sys.executable, "create_distribution.py"], check=True)
    
    print("\nBuild completed successfully!")
    print("You can find the application in the 'Resolume Composition Converter' folder")
    print("or in the 'Resolume Composition Converter.zip' archive.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
