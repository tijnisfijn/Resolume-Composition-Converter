#!/usr/bin/env bash
set -euo pipefail

APP_PATH_PRIMARY="dist/mac/Resolume Composition Converter.app"
APP_PATH_FALLBACK="dist/mac/Resolume Composition Converter/Resolume Composition Converter.app"
APP_PATH_DIST_ROOT="dist/Resolume Composition Converter.app"
DMG_PATH="dist/mac/Resolume-Composition-Converter-macOS.dmg"
VOLUME_NAME="Resolume Composition Converter"

APP_PATH="$APP_PATH_PRIMARY"
if [[ ! -d "$APP_PATH_PRIMARY" && -d "$APP_PATH_FALLBACK" ]]; then
  APP_PATH="$APP_PATH_FALLBACK"
fi
if [[ ! -d "$APP_PATH" && -d "$APP_PATH_DIST_ROOT" ]]; then
  APP_PATH="$APP_PATH_DIST_ROOT"
fi

if [[ ! -d "$APP_PATH" ]]; then
  echo "Missing app bundle at: $APP_PATH_PRIMARY"
  echo "Missing app bundle at: $APP_PATH_FALLBACK"
  echo "Missing app bundle at: $APP_PATH_DIST_ROOT"
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
