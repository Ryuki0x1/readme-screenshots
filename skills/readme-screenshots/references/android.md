# Android Platform Runbook (Kotlin / Jetpack Compose / Java)

> ⚠️ Last machine-verified: 2026-11-02 (Windows host with adb available).
> If you run this successfully on another host, the maintainer would love to
> hear about it — see the "Show it off" section in the repo README.

## Toolchain check (first, before any installing)

```bash
adb version                                            # Android platform-tools
ls ~/.android/avd 2>/dev/null || ls "$ANDROID_HOME"/avd  # emulators present?
```

Policy: never auto-install the Android SDK, `sdkmanager`, a JDK, or an emulator
image (multi-GB downloads the user must consent to). If `adb` is missing, stop
with:

> Android screenshots need ADB, which isn't installed. To enable: install
> Android platform-tools (`winget install Google.PlatformTools` /
> `brew install --cask android-platform-tools`) or Android Studio itself.
> Then say "retry" and continue.

## 1. Device: prefer a real connected phone

```bash
adb devices -l        # any entry in 'device' state beats booting an emulator
```

If a phone is authorized, skip the emulator entirely — faster, and the
screenshots come from real hardware (great for a README).

## 2. Emulator: only if AVDs already exist

If an AVD exists, boot it and wait for full boot:

```bash
emulator -avd <avd_name> -no-snapshot-load &
adb wait-for-device
adb shell 'while [ "$(getprop sys.boot_completed)" != 1 ]; do sleep 2; done'
```

No AVD on disk and no device? Stop and tell the user per the policy above —
downloading a system image is their decision. Simulator-free machines with
nothing to install should be reported honestly, not approximated with markup
mockups.

## 3. Build & install the app

```bash
./gradlew installDebug                            # or :app:installDebug
adb shell pm list packages | grep -i <name-hint>  # discover applicationId
```

## 4. Launch & navigate

```bash
adb shell monkey -p <applicationId> -c android.intent.category.LAUNCHER 1
adb shell am start -n <applicationId>/.MainActivity    # deterministic alternative
```

To reach deep screens, use coordinates from the layout tree (a real, checkable
thing — not guessing):

```bash
adb exec-out uiautomator dump /dev/tty     # XML of visible nodes with bounds
```

Parse `bounds="[x1,y1][x2,y2]"` for the clickable element and tap its center:

```bash
adb shell input tap <cx> <cy>
adb shell input swipe x1 y1 x2 y2 400      # scroll/drag; 400 = ms duration
```

UI transitions animate for roughly 300–500 ms: after each tap take a fresh
layout dump and verify the new state before the next action. Two consecutive
identical dumps is a good rest signal.

## 5. Capture

```bash
sh scripts/capture_android.sh docs/screenshots/hero-home.png
# equivalent inline: adb exec-out screencap -p > docs/screenshots/hero-home.png
```

The phone's own resolution IS the output resolution (e.g. a 1080×2400 device
gives a 1080-wide PNG). In the README cap it around `width="360"` — keep the
full screen including status bar, since that's what users see.

Dark theme: if the app has one, capture both modes:

```bash
adb shell cmd uimode night yes     # then capture dark shots
...
adb shell cmd uimode night no      # restore before finishing
```

## Snags worth expecting

- An app crash mid-navigation resets state — re-launch and re-walk from a
  fresh layout dump instead of tapping blind.
- Debug builds show inspector overlays / build banners. Acceptable for docs;
  if the user wants them gone, a release build is THEIR call (signing).
- Emulator cold boot takes minutes. Wait — nothing is broken.
- Multi-window/split-screen artifacts: finish all captures before fiddling.
