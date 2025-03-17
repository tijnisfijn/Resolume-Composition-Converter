# Changelog

All notable changes to the Resolume Composition Converter will be documented in this file.

## [1.0.3] - 2025-03-17

### Fixed
- Windows build process: Improved robustness of the Windows build process to handle cases where the source package is extracted to a nested directory.
- Windows build instructions: Updated the PC_BUILD_INSTRUCTIONS.md file with clearer instructions and troubleshooting steps for Windows users.

## [1.0.2] - 2025-03-17

### Fixed
- Text component position scaling: Fixed an issue where text component positions (Position X, Position Y) weren't being properly scaled when converting compositions to higher resolutions. This affects all text component types (TextBlock, TextEffect, TextGenerator, BlockTextGenerator).
- Windows build process: Fixed an issue where the Windows build script was trying to run create_windows_icon.py from the wrong location.
- Mac build process: Fixed an issue with the Mac build spec file to ensure the correct path to resolume_gui.py is used.

## [1.0.1] - 2025-03-10

### Added
- Support for preserving aspect ratio for different image formats (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp)
- Improved error handling for file operations

### Fixed
- Fixed an issue with path handling on Windows systems
- Corrected scaling of transform effects for image clips

## [1.0.0] - 2025-02-28

### Added
- Initial release of the Resolume Composition Converter
- Convert Resolume Arena compositions between different resolutions
- Adjust frame rates while preserving timing
- Maintain composition names and structure
- Support for various media types (videos and images)
- Simple and intuitive user interface