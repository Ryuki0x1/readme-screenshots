#!/bin/sh
# Capture the current screen of the booted iOS simulator. macOS only.
# Usage: sh capture_ios.sh docs/screenshots/hero-home.png
set -e

out="$1"
[ -z "$out" ] && { echo "usage: $0 <output.png>" >&2; exit 1; }

if [ "$(uname -s)" != "Darwin" ]; then
  echo "iOS simulator screenshots require macOS. This host cannot produce them." >&2
  exit 2
fi

mkdir -p "$(dirname "$out")"
xcrun simctl io booted screenshot "$out"
echo "saved: $out"
