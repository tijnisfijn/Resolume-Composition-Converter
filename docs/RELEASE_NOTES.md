# Release Notes - Version 1.1.3 (Upcoming)

## New Features
- Added cross-platform CI workflow (Windows + macOS test runs).
- Added release workflow that builds:
  - Windows installer (`.exe`) + portable ZIP
  - macOS DMG + portable ZIP
- Added release notes template automation for GitHub releases.
- Added **Effect Position Rules** manager in app UI:
  - `Help -> Effect Position Rules`
  - lets users review/edit/reset remembered unknown-effect conversion rules.

## Improvements
- Improved conversion coverage for **layer groups** (group transform and sizing handling).
- Added smarter conversion for non-transform effects with position/anchor parameters.
- Added explicit pixel conversion support for `ScreenLayerTransform` (including small values).
- Expanded README and install docs with beginner-friendly build-from-source steps.
- Updated manual and generated HTML documentation for the new behavior.

## Technical Updates
- Added Inno Setup installer script for Windows CI builds.
- Added macOS DMG creation script for CI builds.
- Removed deprecated artifact action usage from old workflow path.

---

# Release Notes - Version 1.1.2

## Improvements
- Removed drag and drop functionality to improve stability
- Fixed issue with file conversion not working properly
- Improved file overwrite warning behavior to avoid duplicate warnings
- Streamlined the user interface for better usability

## Bug Fixes
- Fixed issue where the application was creating a copy of the original file instead of converting it
- Fixed redundant warning messages when overwriting existing files
- Removed leftover drag and drop code that was causing errors

## Technical Updates
- Reduced code complexity by removing unused features
- Improved error handling throughout the application

---

# Release Notes - Version 1.1.1

## New Features
- Added automatic update checker functionality
- Added "Check for Updates" option in the Help menu
- Implemented silent update checking on application startup
- Created user-friendly update notification dialogs

## Improvements
- Implemented centralized version management system
- Enhanced error handling for network issues
- Added browser integration to open download page for updates

## Technical Updates
- Added requests library for API communication
- Improved application startup sequence
- Enhanced menu organization

## Documentation
- Updated documentation to reflect new update checker functionality
- Added version information to About dialog

---

Thank you for using Resolume Composition Converter!
