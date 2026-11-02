<div align="center">

# 📸 readme-screenshots

**An AI-agent skill that documents your app with real screenshots and a beautiful README.**

Point any AI agent at any project and say *"document it with screenshots"* —
the agent will run your app, capture its UI for real, and produce a vibrant,
clean `README.md` that showcases it.

**Follows the open skills spec, so it works with:** Claude Code · OpenCode ·
Codex CLI · Cursor · Gemini CLI — anything that reads `SKILL.md`.

Works with web apps, websites, static pages, browser extensions — and native
projects on familiar ground for that platform:

| Platform | How it captures | Requirements |
| :--- | :--- | :--- |
| 🌐 Web app / website / static page | Headless Chromium (Playwright) | Python + Playwright (small, auto-noted if missing) |
| 🧩 Browser extension (MV3) | Extension pages served & captured as web pages | same |
| 🤖 Android (Kotlin/Jetpack) | `adb` screencap from a connected phone or an existing emulator | Android platform-tools + a device/AVD you already have |
| 🍎 iOS (Swift) | `xcrun simctl` screenshots from the iOS Simulator | **macOS + Xcode** — hard requirement, stated honestly |
| 🎯 Flutter | Routes to whichever target you have (Android device, web-server build, iOS sim) | per target |

**Design promise:** the skill uses toolchains that already exist on your
machine and never silently downloads multi-gigabyte SDKs. If something's
missing (Android SDK, Xcode), it stops with the exact one-line fix instead of
pretending.

</div>

---

## Install (any agent)

Any agent that supports the open [skills](https://skills.sh) format — Claude
Code, Codex, Cursor, Gemini CLI, OpenCode:

```bash
npx skills add Ryuki0x1/readme-screenshots
```

Manual install — clone or copy the `skills/readme-screenshots/` folder into
whatever your agent reads:

| Agent / tool | Destination |
| :--- | :--- |
| OpenCode (global) | `~/.agents/skills/` (or your configured Agent Skills dir) |
| OpenCode (per-project, temporary) | `.opencode/skills/` |
| Claude Code | `~/.claude/skills/` |
| Any agent | point it at `SKILL.md` and let it follow the workflow |

## Use it

```text
> Document this project with screenshots
> Make my README show off the app
> Add screenshots to my readme
```

You can narrow it too: *"…but only the settings page, dark mode."*

## Layout

```
skills/readme-screenshots/
├── SKILL.md            ← the workflow: platform detection → runbook → capture → README
├── references/
│   ├── web.md          # websites, dev servers, static pages, extensions
│   ├── android.md      # adb device or emulator; UI navigation via uiautomator
│   ├── ios.md          # macOS + Xcode Simulator; refuses politely elsewhere
│   └── flutter.md      # routes to android / web / ios targets
└── scripts/
    ├── capture_web.py      # --url --out --selector --fullpage --dark --set ...
    ├── capture_android.sh  # adb exec-out screencap
    └── capture_ios.sh      # xcrun simctl io booted screenshot
```

## Honest status

- ✅ Web / static / extension path: machine-verified in production use
  (screenshots of a browser extension shipped from this very workflow).
- ⚠️ Android / iOS / Flutter runbooks: authored and reviewed, not yet run on
  this maintainer's machine (no emulator handy / no Mac). Each runbook is
  marked with its verification status and expected to be battle-tested in
  public — that's where you come in 👇

## Show it off ⭐

Did this skill work on your machine — especially an
**Android phone, iOS Simulator, or Flutter target** the maintainer couldn't
test? Please:

- ⭐ **Star this repo** so others find it, and/or
- 🍴 **Fork it and showcase your result** — open your README or a PR with the
  platforms you verified; runbook corrections (commands, flags, quirks) are
  the most valuable kind.

Real-world reports from different machines are exactly what turns the ⚠️ rows
in the status table into ✅.

## License

MIT — see [LICENSE](LICENSE).
