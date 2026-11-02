# Web Platform Runbook (websites, dev servers, static pages, browser extensions)

Covers anything that renders in a browser: web apps with a dev server, static
HTML pages, and WebExtension (MV3/MV2) popup/options/overlay pages.

## Prerequisites (check, don't install blindly)

- A browser-capable capture tool. Bundled: `scripts/capture_web.py`
  (Playwright + Chromium). Check with:
  ```bash
  python -c "from playwright.sync_api import sync_playwright; print('ok')"
  ```
- Playwright missing? Install it (small, safe to auto-install unlike native
  SDKs): `pip install playwright && python -m playwright install chromium`
- Alternative if the agent has its own browser tool: use it following the same
  conventions (natural shape, wait for render).

## 1. Dev-server app (React/Vite/Next etc.)

Read `package.json`; find the dev script and the port it prints. Start it in
the background and WAIT until the port answers before opening pages — a 200
response matters more than the "Listening…" message when there are on-demand
compile steps:

```bash
npm run dev &    # note the printed port
# poll: curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT
```

If a build step takes a while, that's normal — wait. If the app needs env
secrets or credentials it doesn't have, don't hack around them; capture the
pages that do render and note it to the user.

## 2. Static pages

Serve the folder rather than using `file://` — file URLs break fonts, CORS,
and relative-root assets:

```bash
python3 -m http.server 8900 --directory <folder>   # keep alive until captures done
```

## 3. Browser extension pages

Open the extension's HTML pages (popup, options, paused/placeholder pages)
normal web pages. Expectations to set before capturing:

- `chrome.*` / `browser.*` APIs do NOT exist outside the extension runtime.
  Dynamic fields (live counters, tab lists, storage-backed settings) stay
  empty/frozen — that's fine; capture the layout as rendered.
- Some pages read URL params (e.g. placeholder pages take `?title=&url=`).
  Read the project's JS to find these and pass realistic values — it makes
  placeholder shots look alive.
- Inject demo state via JS at runtime for hero shots (counters, selected tab
  title/domain) so the page doesn't show "Loading…" — and disclose it.
- Anything that auto-writes to its own DOM on an interval: inject your values
  AFTER the app's own render attempt, or capture immediately after injection.

## Capturing with the bundled script

```bash
# element shot at natural size (dialogs, popups)
python scripts/capture_web.py --url http://localhost:8900/popup.html \
  --out docs/screenshots/hero-popup.png --selector ".container" --dark

# full page at desktop size
python scripts/capture_web.py --url http://localhost:3000/settings \
  --out docs/screenshots/settings.png --fullpage --dark

# with demo state injected right before capture
python scripts/capture_web.py --url http://localhost:3000 \
  --out docs/screenshots/hero.png --set "document.querySelector('#count').textContent='42'"
```

The script waits for `load` + fonts, applies `--set` JS (repeatable), and
supports `--selector` element capture, `--fullpage`, `--width/--height`,
`--dark` (forces `prefers-color-scheme: dark` — this flips CSS themes for apps
that support dark-by-default styling), and `--dpr 2` (retina, the default).

Viewport discipline: query the app for its natural size when it matters. A
browser-extension popup is usually 320–420 CSS px wide — check its CSS — and
the element shot keeps it authentic. Hand-cropping is a last resort and
banned: crop coordinates must come from a measured bounding rect, not eyes.

Local file + query params: pass them full through `--url`, e.g.
`file:///path/page.html?title=Demo` only if `file://` works for that page;
otherwise register it on the static server.
