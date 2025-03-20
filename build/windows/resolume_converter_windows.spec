# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Get the repository root directory
import os
import sys

# Print current directory for debugging
print(f"Current directory: {os.getcwd()}")
print(f"Spec file directory: {os.path.dirname(SPECPATH)}")

# Try to find resolume_gui.py in various locations
possible_locations = [
    # Standard location (same directory as build/windows)
    os.path.abspath(os.path.join(os.path.dirname(SPECPATH), "../..")),
    # Current directory
    os.getcwd(),
    # Parent directory (for nested extractions)
    os.path.dirname(os.getcwd()),
    # Explicit path based on extraction pattern
    os.path.dirname(os.path.dirname(os.getcwd()))
]

# Find the first location that contains src/resolume_gui.py
repo_root = None
for location in possible_locations:
    test_path = os.path.join(location, 'src/resolume_gui.py')
    print(f"Testing path: {test_path}")
    if os.path.exists(test_path):
        repo_root = location
        print(f"Found src/resolume_gui.py at: {repo_root}")
        break

# If we couldn't find it, use the current directory as a fallback
if repo_root is None:
    repo_root = os.getcwd()
    print(f"WARNING: Could not find src/resolume_gui.py, using current directory: {repo_root}")

# Add the MANUAL.md and screenshots to the data files
datas = [
    (os.path.join(repo_root, 'docs/MANUAL.md'), '.'),
    (os.path.join(repo_root, 'screenshots/app_screenshot.png'), 'screenshots')
]

a = Analysis(
    [os.path.join(repo_root, 'src/resolume_gui.py')],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[os.path.join(repo_root, 'src/runtime_hook.py')],  # Add our runtime hook
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Resolume Composition Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(repo_root, 'icons/app_icon.ico'),  # Windows icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Resolume Composition Converter',
)