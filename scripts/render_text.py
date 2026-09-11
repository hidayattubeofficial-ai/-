"""Render Urdu Nastaliq text through Chromium's native RTL/complex-text shaping."""
from pathlib import Path
from html import escape
import asyncio
import sys

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "video_text.html"

async def render(title: str, body: str, footer: str, output_png: str) -> None:
    template = TEMPLATE.read_text(encoding="utf-8")
    html = template.replace("__TITLE__", escape(title))
    html = html.replace("__BODY__", escape(body).replace("\n", "<br>"))
    html = html.replace("__FOOTER__", escape(footer))

    temp_html = ROOT / "output" / "_video_text_runtime.html"
    temp_html.write_text(html, encoding="utf-8")
    out = Path(output_png)
    out.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--font-render-hinting=none"])
        page = await browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        await page.goto(temp_html.as_uri(), wait_until="load")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(500)
        loaded = await page.evaluate("document.fonts.check('52px \\\"Noto Nastaliq Urdu\\\"')")
        if not loaded:
            raise RuntimeError("Noto Nastaliq Urdu did not load in Chromium")
        await page.screenshot(path=str(out), omit_background=True, full_page=False)
        await browser.close()

    temp_html.unlink(missing_ok=True)
    print(f"Verified Chromium Urdu shaping and saved: {out}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit("Usage: render_text.py TITLE BODY FOOTER OUTPUT_PNG")
    asyncio.run(render(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
