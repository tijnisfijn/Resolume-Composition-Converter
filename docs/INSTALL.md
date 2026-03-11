# Installation Guide

This guide covers both prebuilt releases and building from source.

## Prebuilt Releases (Recommended)

Download the latest artifacts from:
- [Releases Page](https://github.com/tijnisfijn/Resolume-Composition-Converter/releases)

### Windows

1. Download `Resolume-Composition-Converter-Setup.exe` (installer) or `Resolume Composition Converter Windows.zip` (portable).
2. For installer: run the `.exe` and follow the wizard.
3. For portable ZIP: extract and run `Resolume Composition Converter.exe`.

SmartScreen note:
- The installer is currently not code-signed.
- Windows may show a SmartScreen warning.
- Use `More info -> Run anyway` if you trust the release.

### macOS

1. Download `Resolume-Composition-Converter-macOS.dmg` or `Resolume Composition Converter Mac.zip`.
2. DMG: open it, then drag the app to Applications.
3. ZIP: extract, then move `Resolume Composition Converter.app` to Applications.

Gatekeeper note:
- The app is currently not notarized.
- First launch may be blocked.
- Right-click app -> `Open` -> `Open`.

## Build From Source

Prerequisites:
- Python 3.10+
- Python installation with working `tkinter`/Tcl-Tk
- `pip`

### Windows

```powershell
git clone https://github.com/tijnisfijn/Resolume-Composition-Converter.git
cd Resolume-Composition-Converter
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python build/windows/build_windows.py
```

Output:
- `dist/windows/Resolume Composition Converter`
- `dist/windows/Resolume Composition Converter Windows.zip`

### macOS

```bash
git clone https://github.com/tijnisfijn/Resolume-Composition-Converter.git
cd Resolume-Composition-Converter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python build/mac/build_mac.py
bash scripts/create_macos_dmg.sh
```

Output:
- `dist/mac/Resolume Composition Converter.app`
- `dist/mac/Resolume Composition Converter Mac.zip`
- `dist/mac/Resolume-Composition-Converter-macOS.dmg`

## Verify Build/Test

```bash
python scripts/run_tests.py
```

## Documentation

- User manual: `docs/MANUAL.md`
- Generated manual HTML: `documentation/MANUAL.html`
