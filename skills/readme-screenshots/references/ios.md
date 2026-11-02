# iOS Platform Runbook (Swift / SwiftUI / UIKit — macOS only)

> ⚠️ Last machine-verified: never (authored on a Windows host; the capture
> method is standard `xcrun simctl` usage). If you run this successfully,
> please report back / star the repo — see "Show it off" in the README.

## Hard gate: host OS

If the host is not macOS (check `uname -s`), stop after one honest sentence:

> iOS app screenshots require macOS (Xcode Simulator). This machine can't run
> them. Two options: run this task on a Mac, or capture screenshots yourself
> on the simulator and drop them in `docs/screenshots/` — I'll compose the
> README around whatever is there).

No amount of retrying changes this. Do not propose workarounds that "simulate"
an iPhone.

## Toolchain check (on macOS)

```bash
xcodebuild -version
xcrun simctl list devices available    # shows booted/available simulators
```

Missing Xcode? It's from the App Store / `xcode-select --install` for the CLI
tools — a user decision, multi-GB; state it, don't auto-install.

## 1. Boot a simulator (if none is booted)

```bash
xcrun simctl list devices available | grep -m1 iPhone
xcrun simctl boot "<device-name>"
xcrun simctl bootstatus "<device-name>" -b    # waits for full boot
xcrun simctl launch booted <bundle.id>
```

## 2. Build & install the app

Prefer building a scheme into the booted sim:

```bash
xcodebuild -list                       # discover scheme(s)
xcodebuild -scheme <Scheme> -destination 'platform=iOS Simulator,name=<device-name>' build
xcrun simctl install booted <path/to/built.app>   # from DerivedData/Build/Products/Debug-iphonesimulator
```

If the project builds via Xcode GUI or needs signing the agent can't complete,
say so and hand that single step to the user — never skip it silently.

## 3. Capture

```bash
sh scripts/capture_ios.sh docs/screenshots/hero-home.png
# equivalent: xcrun simctl io booted screenshot docs/screenshots/hero-home.png
```

Output is the sim's native pixel size (e.g. 1179×2556 for iPhone 15 Pro). In
the README cap at `width="360"`.

Dark mode (if the app supports it — check asset catalogs / SwiftUI
`preferredColorScheme`):

```bash
xcrun simctl ui booted appearance dark     # capture shots
xcrun simctl ui booted appearance light    # restore after
```

## 4. Navigate inside the app

The simulator is a full UI: click coordinates with `simctl io` is limited —
the reliable path is launching deep links (`simctl openurl booted myapp://…`)
if the app registers URL schemes, or tapping coordinates in the simulator
GUI window via AppleScript (fragile). Prefer app-defined deep links; if
neither exists, screenshot the screens reachable by default launch and ask
the user to tap-through remaining ones (or accept fewer shots).
