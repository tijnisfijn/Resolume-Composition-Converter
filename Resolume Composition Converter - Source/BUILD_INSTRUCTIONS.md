# Build Instructions for Windows

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
   venv\Scripts\activate
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
