---
name: readme-screenshots
description: >-
  Turns a software project into a polished, visual README by running the app,
  capturing REAL screenshots of its UI, and composing a vibrant, clean
  README.md around them. Works across platforms: websites and dev servers,
  static pages, browser extensions, Kotlin/Android apps, iOS (macOS only),
  and Flutter. Use this skill whenever the user wants to "add screenshots to
  my README", "make my README look good", "generate docs with screenshots",
  "showcase my app/project", "make a visual guide", or when a repo has an
  interface and the user asks for documentation, presentation, or any
  README-adjacent polish — even if they never say the word "screenshots".
  Trigger generously: a good README with real screenshots beats a bare one in
  every codebase.
---

# README Screenshots

Turn a working project into a documented, visual one: run the app, capture real
screenshots of its surfaces, and compose a vibrant, clean `README.md` around
them. The result should read like the landing page of a well-loved open source
project.

Non-negotiables, whatever the platform:

- Screenshots are REAL captures of the running app. Never draw, mock up, or
  fake an image.
- They live in the repo (`docs/screenshots/`) and the README references them
  with relative paths so they render on GitHub.
- Nothing destructive: never modify the project's source code to make a
  screenshot happen — inject demo state at runtime if needed, then say so.

## Workflow

### Phase 1 — Detect the platform

Look for these signals in the project root, then load ONE runbook from
`references/`:

| Signals | → Runbook |
| :--- | :--- |
| `package.json` with a dev/start script, or `index.html`, or a pure web frontend in a `src`/`public` folder | `references/web.md` |
| `manifest.json` (WebExtension/MV3/V2) | `references/web.md` (extension section) |
| Android: `build.gradle(.kts)`, `AndroidManifest.xml`, `settings.gradle`, Kotlin/Java app sources | `references/android.md` |
| iOS: `*.xcodeproj`, `*.xcworkspace`, `Info.plist`, app code in Swift | `references/ios.md` |
| Flutter: `pubspec.yaml` with `flutter:` and `lib/main.dart` | `references/flutter.md` |
| Multiple platforms (e.g. Flutter + native, or a monorepo) | document the flagship UI's platform first; note the others in the README |

If the platform is genuinely ambiguous, ask the user once with your best parse
of the repo surfaced. If the project has NO user-visible interface (pure
library/CLI), don't fake UI shots — fall back to a terminal demo, a refined
diagram, or a generated banner, and still produce a great README.

### Phase 2 — Run the app per the runbook

Each runbook tells you:

1. What must already exist on this machine (toolchain check, repeatable one-line
   command).
2. How to boot the app so its UI renders.
3. How to actually capture pixels (bundled script in `scripts/` or a native
   capture command).
4. How to recover when something's blank ("wait for render" beats "retry
   blind").

### Phase 3 — Capture

Conventions that apply on every platform:

- Save into `<repo>/docs/screenshots/`, kebab-case names that describe the
  moment (`hero-dashboard.png`, `settings-screen.png`), never the tool
  (`screenshot-2026-01-04-14-22.png`).
- Capture each surface at its natural shape: dialogs/popups at their native
  size, pages at 1280×800 or full page. On phones, capture the device screen
  as-is (its own resolution is part of the story).
- Prefer dark mode for the hero shot when the app has one — dark UIs pop in
  READMEs — but only if it has a real dark theme; don't force one.
- Staged demo state is allowed (empty counters, "Loading…" placeholders look
  broken in marketing shots), but it must be injected at runtime, not written
  into project code, and you must discose it to the user in your summary.
- A blank or flickering frame is a timing bug, not the app's fault: wait for
  load + a beat for fonts/icons/transitions, retry once with a longer wait.

### Phase 4 — Compose the README

Write (or rewrite) `README.md` at the repo root. If rich readme content already
exists (`git-readme.md`, a prose file, docs), mine ALL its facts — you are
upgrading presentation, never deleting information.

Target structure (adapt freely, keep it scannable):

```markdown
# <Project Name>
<p align="center"><img src="docs/screenshots/hero.png" width="…"></p>
> One-sentence pitch with personality.
badges: license, language, install link
## Why it exists        ← the pain, 2–4 lines, bold numbers if real
## What it does         ← ✨ tight feature list (+ shots next to their features)
## Screenshots tour     ← gallery with one-line captions
## How it works         ← architecture in plain words; tables over prose
## Installation         ← numbered, copy-pasteable
## Configuration        ← parameter table if the app has settings
## Privacy / Safety     ← only when meaningful
## License
```

Style rules:

- Hero shot above the fold, explicit width (`width="400"` for phone shots,
  under ~728px for desktop) so it lays out well on GitHub.
- One idea per section; short paragraphs; bold only for scanning aids.
- Tables for compatibility matrices and settings — they beat prose.
- Minimal, tasteful emoji in headers (⏱ 🎨 🚀) is fine; don't salt every line.
- Relative image paths with alt text, always.
- Never narrate the screenshotting process in the README; it reads as if the
  project itself wrote it.

### Phase 5 — Verify

- Every image path in the README resolves to an existing file.
- No screenshot over ~1.5 MB; compress (PNG → WebP or downscale) if bigger.
- Tell the user: where the README is, which shots exist, which ones carry
  demo-injected values, and offer to swap the hero choice, theme, or order.

## Toolchain policy (missing-dependency handling)

The skill uses whatever toolchain already exists on the machine and NEVER
silently installs platform SDKs (Android SDK, Xcode, Android emulators —
multi-GB downloads the user must consent to). If a runbook's toolchain check
fails, stop cleanly with exactly this shape:

> [Platform] screenshots need [tool], which isn't installed. To enable it:
> `<exact install command or step>`. Install it, then say "retry" and I'll
> continue — the work done so far (detection, README skeleton) is saved.

iOS is a special case: if the host is not macOS, say so in one sentence and
skip — no retry can enable it on Windows/Linux. Offer the user the option of
providing screenshots they captured themselves.
