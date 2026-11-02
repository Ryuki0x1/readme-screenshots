#!/bin/sh
# Capture the current screen of an Android device or emulator.
# Usage: sh capture_android.sh docs/screenshots/hero-home.png [device-serial]
set -e

out="$1"
serial="$2"

if [ -z "$out" ]; then
  echo "usage: $0 <output.png> [device-serial]" >&2
  exit 1
fi

adb_flags=""
[ -n "$serial" ] && adb_flags="-s $serial"

# verify a device is actually there
devices=$(adb $adb_flags devices | awk 'NR>1 && $2=="device"' | wc -l | tr -d ' ')
if [ "$devices" -eq 0 ]; then
  echo "No Android device in 'device' state. Run 'adb devices' to check USB debugging authorization." >&2
  exit 2
fi

mkdir -p "$(dirname "$out")"
adb $adb_flags exec-out screencap -p > "$out"
echo "saved: $out"
