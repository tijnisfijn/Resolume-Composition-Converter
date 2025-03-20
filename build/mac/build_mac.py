#!/usr/bin/env python3
"""
Build script for macOS
"""

import os
import sys
import subprocess
import shutil

def main():
    """Main function"""
    print("Building Resolume Composition Converter for macOS...")
    
    # Get the repository root directory
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    print(f"Repository root directory: {repo_root}")
    
    # Change to the repository root directory
    os.chdir(repo_root)
    print(f"Current working directory: {os.getcwd()}")
    
    # Activate virtual environment if not already activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Virtual environment not activated. It's recommended to run this script in a virtual environment.")
    
    # Install requirements
    print("\nInstalling requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Build the application
    print("\nBuilding application with PyInstaller...")
    subprocess.run([sys.executable, "-m", "PyInstaller", "build/mac/resolume_converter.spec"], check=True)
    
    # Create HTML documentation
    print("\nCreating HTML documentation...")
    subprocess.run([sys.executable, "convert_manual_simple.py"], check=True)
    
    # Create distribution package
    print("\nCreating distribution package...")
    subprocess.run([sys.executable, "create_distribution.py"], check=True)
    
    # Move the built application to the dist/mac directory
    if os.path.exists("dist/Resolume Composition Converter"):
        if os.path.exists("dist/mac/Resolume Composition Converter"):
            shutil.rmtree("dist/mac/Resolume Composition Converter")
        shutil.move("dist/Resolume Composition Converter", "dist/mac/")
        print("\nMoved built application to dist/mac/")
    
    if os.path.exists("Resolume Composition Converter.app"):
        if os.path.exists("dist/mac/Resolume Composition Converter.app"):
            shutil.rmtree("dist/mac/Resolume Composition Converter.app")
        shutil.move("Resolume Composition Converter.app", "dist/mac/")
        print("Moved application bundle to dist/mac/")
    
    if os.path.exists("Resolume Composition Converter.zip"):
        if os.path.exists("dist/mac/Resolume Composition Converter.zip"):
            os.remove("dist/mac/Resolume Composition Converter.zip")
        shutil.move("Resolume Composition Converter.zip", "dist/mac/")
        print("Moved ZIP archive to dist/mac/")
    
    print("\nBuild completed successfully!")
    print("You can find the application in the 'dist/mac/Resolume Composition Converter' folder")
    print("or in the 'dist/mac/Resolume Composition Converter.zip' archive.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())