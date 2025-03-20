#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Launch the application
"$SCRIPT_DIR/Resolume Composition Converter.app/Contents/MacOS/Resolume Composition Converter" "$@"