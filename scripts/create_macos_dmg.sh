#!/usr/bin/env bash
set -euo pipefail

APP_PATH="dist/mac/Resolume Composition Converter.app"
DMG_PATH="dist/mac/Resolume-Composition-Converter-macOS.dmg"
VOLUME_NAME="Resolume Composition Converter"

if [[ ! -d "$APP_PATH" ]]; then
  echo "Missing app bundle at: $APP_PATH"
  exit 1
fi

mkdir -p "dist/mac"
rm -f "$DMG_PATH"

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

cp -R "$APP_PATH" "$TMP_DIR/"

hdiutil create \
  -volname "$VOLUME_NAME" \
  -srcfolder "$TMP_DIR" \
  -ov \
  -format UDZO \
  "$DMG_PATH"

echo "Created DMG: $DMG_PATH"
