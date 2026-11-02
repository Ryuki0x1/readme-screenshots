# Flutter Platform Runbook

Flutter is not its own capture pipeline — it wins by routing to a target that
already works. Detect available targets first, then follow the OTHER runbook's
capture steps.

> ⚠️ Runbooks are instruction-of-record; last full cross-check 2026-11-02.

## 1. Discover targets

```bash
flutter devices
```

Decision order (first available wins):

| Available target | Route to | Capture method |
| :--- | :--- | :--- |
| Android device/emulator (`adb devices` shows one) | `references/android.md` | adb screencap |
| Chrome/Edge + `flutter run -d web-server` works | web-flavored capture | Playwright |
| macOS host + iOS sim booted | `references/ios.md` | simctl |

## 2. Boot the app

**Android target:** build & install with the app module's own commands:

```bash
flutter build apk --debug
adb install -r build/app/outputs/flutter-apk/app-debug.apk
```

then continue in `references/android.md` from "Launch & navigate".

**Web target (needs no device at all):**

```bash
flutter run -d web-server --web-port 8123 --web-hostname localhost
```

Wait for "This app is linked" / the port to answer, then treat it EXACTLY like
a web app: `references/web.md` Phase 2/3 — serve not required (the dev server
is the serve), use `scripts/capture_web.py`.

Caveats specific to Flutter web: fonts/icons come as web assets — extra wait
after `load` (the script handles fonts). Canvas-rendered UIs respond to
`--selector` fine (they're regular DOM elements); if the app renders to a raw
canvas with no containers, drop `--selector` and use default viewport.

**iOS target:** only after the iOS runbook's macOS gate passes.

## 3. State & demo values

Flutter hot-reloads are irrelevant for one-shot capture; prefer launching the
app in the target state you want (deep link, or `flutter run --dart-define`s
the app supports) over driving UI inside it. If the UI must be driven, note
that Flutter web Supports Playwright `page.click`/`fill` normally (it's a
Flutter widget = DOM elements on web target) — much easier than clicking on
Android canvases.

## 4. Compose

Screens from any target go to the same `docs/screenshots/` and same README
rules (SKILL.md Phase 3–5). If shots mix platforms (android + web), caption
each shot with what it is; that's informative, not confusing.
