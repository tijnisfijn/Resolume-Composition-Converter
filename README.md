# Resolume Composition Converter
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/tijnisfijn/Resolume-Composition-Converter/actions/workflows/ci.yml/badge.svg)](https://github.com/tijnisfijn/Resolume-Composition-Converter/actions/workflows/ci.yml)
[![Release Installers](https://github.com/tijnisfijn/Resolume-Composition-Converter/actions/workflows/release-installers.yml/badge.svg)](https://github.com/tijnisfijn/Resolume-Composition-Converter/actions/workflows/release-installers.yml)

Adapt existing Resolume Arena `.avc` compositions to new resolution, framerate, and media paths without rebuilding your show from scratch.

![Resolume Composition Converter Banner](screenshots/banner.jpg)

## Cool Things You Can Do
- Convert HD compositions to 4K while keeping clip/layer/group layout intact.
- Move from `30 fps` to `60 fps` while preserving timing behavior.
- Swap media roots in bulk (`Old File Path` -> `New File Path`).
- Replace formats by basename (`clip1.mp4` -> `clip1.mov` / `clip1.dvx`) with `Ignore file extensions`.
- Preserve and scale transform/anchor parameters across composition, groups, layers, and clips.
- Handle unknown position-based effects once, then reuse remembered rules automatically.

## How It Works
The app edits the XML inside your `.avc` and applies deterministic conversions:
- Resolution scaling:
  position and anchor parameters are scaled by width/height factors.
- Framerate conversion:
  timing-related values are adjusted to keep perceived playback behavior consistent.
- Media path remap:
  references are rewritten from old root to new root, with optional extension-agnostic matching.
- Effect position memory:
  when an unknown effect has position/anchor semantics, you choose `Convert` or `Skip`; that policy is saved and reused.

This lets you keep your creative structure while adapting technical delivery requirements.

## Download
- Latest release: [Releases](https://github.com/tijnisfijn/Resolume-Composition-Converter/releases/latest)

### Windows
1. Download `Resolume-Composition-Converter-Setup.exe` (recommended), or `Resolume Composition Converter Windows.zip`.
2. Install (or unzip) and launch `Resolume Composition Converter.exe`.

### macOS
1. Download `Resolume-Composition-Converter-macOS.dmg` (recommended), or `Resolume Composition Converter Mac.zip`.
2. Install (or unzip) and move app to `Applications`.

## First-Run Notes
- Windows SmartScreen warning is expected for unsigned binaries:
  click `More info` -> `Run anyway`.
- macOS Gatekeeper warning is expected for non-notarized app:
  right-click app -> `Open` -> `Open`.

## Quick Start
1. Open app.
2. Select input `.avc`.
3. Select output `.avc`.
4. Confirm original settings.
5. Set target resolution/framerate.
6. Optional: set old/new media roots and enable `Ignore file extensions`.
7. Click `Convert Composition`.

## Documentation
- Full manual (Markdown): [docs/MANUAL.md](docs/MANUAL.md)
- Full manual (HTML): [documentation/MANUAL.html](documentation/MANUAL.html)
- Install guide: [docs/INSTALL.md](docs/INSTALL.md)
- Issues / bug reports: [GitHub Issues](https://github.com/tijnisfijn/Resolume-Composition-Converter/issues)

## Build From Source
Prerequisites:
- Python `3.10+`
- Python with working `tkinter` / Tcl-Tk
- `pip`
- `git`

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

Outputs:
- `dist/windows/Resolume Composition Converter Windows.zip`
- `dist/windows/installer/Resolume-Composition-Converter-Setup.exe` (when installer step runs)

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

Outputs:
- `dist/mac/Resolume Composition Converter Mac.zip`
- `dist/mac/Resolume-Composition-Converter-macOS.dmg`

## CI/CD
- CI workflow: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)
- Release installer workflow: [`.github/workflows/release-installers.yml`](.github/workflows/release-installers.yml)
- Tag format: `vX.Y.Z` to publish a release.

## Contributing
1. Open an issue for bug/feature discussion.
2. Create a branch and implement changes.
3. Run tests.
4. Open PR.

## License
MIT — see [LICENSE](LICENSE).
