"""Render Urdu Nastaliq text and Hidayat Tube branding through Chromium."""
from pathlib import Path
from html import escape
import asyncio
import sys

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "video_text.html"
CTA_TEMPLATE = ROOT / "cta_only.html"
LOGO = ROOT / "assets" / "branding" / "logo.png"

async def _render_template(template_path: Path, replacements: dict[str, str], output_png: str) -> None:
    template = template_path.read_text(encoding="utf-8")
    replacements = dict(replacements)
    replacements["__LOGO__"] = LOGO.resolve().as_uri()
    for key, value in replacements.items():
        template = template.replace(key, escape(value))

    temp_html = ROOT / "output" / "_video_text_runtime.html"
    temp_html.write_text(template, encoding="utf-8")
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

        # The full scene template contains the branding logo, while the CTA-only
        # overlay intentionally does not. Validate the logo only when that
        # template actually includes a .brand-logo element.
        logo_locator = page.locator(".brand-logo")
        if await logo_locator.count():
            logo_loaded = await logo_locator.evaluate("el => el.complete && el.naturalWidth > 0")
            if not logo_loaded:
                raise RuntimeError(f"Hidayat Tube branding logo did not load: {LOGO}")

        await page.screenshot(path=str(out), omit_background=True, full_page=False)
        await browser.close()

    temp_html.unlink(missing_ok=True)
    print(f"Verified Chromium Urdu shaping + Hidayat Tube branding and saved: {out}")

async def render(title: str, body: str, footer: str, output_png: str) -> None:
    await _render_template(TEMPLATE, {"__TITLE__": title, "__BODY__": body, "__FOOTER__": footer}, output_png)

async def render_cta(output_png: str) -> None:
    await _render_template(CTA_TEMPLATE, {}, output_png)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        asyncio.run(render(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    elif len(sys.argv) == 3 and sys.argv[1] == "--cta":
        asyncio.run(render_cta(sys.argv[2]))
    else:
        raise SystemExit("Usage: render_text.py TITLE BODY FOOTER OUTPUT_PNG | render_text.py --cta OUTPUT_PNG")
