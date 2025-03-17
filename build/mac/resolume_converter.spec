# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Get the repository root directory
import os
# Use hardcoded path to ensure correct location
repo_root = '/Users/tijn/Code/UpscaleComp'
print(f"Repository root directory: {repo_root}")

# Use absolute path for the main script
main_script = os.path.join(repo_root, 'resolume_gui.py')
print(f"Main script path: {main_script}")

# Add the MANUAL.md and screenshots to the data files
datas = [
    (os.path.join(repo_root, 'MANUAL.md'), '.'),
    (os.path.join(repo_root, 'screenshots/app_screenshot.png'), 'screenshots')
]

a = Analysis(
    [main_script],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[os.path.join(repo_root, 'runtime_hook.py')],  # Add our runtime hook
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
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(repo_root, 'icons/app_icon.icns'),  # macOS icon
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

app = BUNDLE(
    coll,
    name='Resolume Composition Converter.app',
    icon=os.path.join(repo_root, 'icons/app_icon.icns'),
    bundle_identifier='com.tijnisfijn.resolume-composition-converter',
    info_plist={
        'CFBundleShortVersionString': '1.0.2',
        'CFBundleVersion': '1.0.2',
        'NSHighResolutionCapable': 'True',
        'NSHumanReadableCopyright': '© 2025 Tijn Schuurmans',
    },
)