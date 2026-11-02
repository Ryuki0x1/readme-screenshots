#!/usr/bin/env python3
"""Capture a screenshot of a web page (element or full-page) with headless Chromium.

Examples:
  python capture_web.py --url http://localhost:8900/popup.html --out shot.png --selector ".container" --dark
  python capture_web.py --url http://localhost:3000/settings --out settings.png --fullpage --height 900
  python capture_web.py --url http://localhost:3000 --out hero.png \
      --set "document.getElementById('count').textContent='42'" --set "more JS..."
"""
import argparse
from playwright.sync_api import sync_playwright


def main():
    p = argparse.ArgumentParser(description="Capture a web page screenshot.")
    p.add_argument("--url", required=True)
    p.add_argument("--out", required=True, help="output PNG path")
    p.add_argument("--selector", help="capture the matching element instead of the viewport/full page")
    p.add_argument("--fullpage", action="store_true", help="capture entire scrollable page")
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=800)
    p.add_argument("--dpr", type=int, default=2, help="device scale factor (2 = retina)")
    p.add_argument("--dark", action="store_true", help="emulate prefers-color-scheme: dark")
    p.add_argument("--set", dest="inject", action="append", default=[],
                   metavar="JS", help="JS expression to run before capture (repeatable)")
    p.add_argument("--wait", type=int, default=400, help="extra ms to wait after load")
    args = p.parse_args()

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.dpr,
            color_scheme="dark" if args.dark else "light",
        )
        page = ctx.new_page()
        page.goto(args.url)
        page.wait_for_load_state("load")
        page.evaluate("document.fonts.ready.then(() => true)")
        for js in args.inject:
            page.evaluate(js)
        page.wait_for_timeout(args.wait)

        if args.selector:
            page.locator(args.selector).first.screenshot(path=args.out)
        else:
            page.screenshot(path=args.out, full_page=args.fullpage)
        browser.close()
    print("saved:", args.out)


if __name__ == "__main__":
    main()
