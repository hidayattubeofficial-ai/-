"""Build Hadith #001 long-form review video from the official Dawat-e-Islami source."""
from pathlib import Path
import asyncio
import re
import subprocess
import sys
from html import escape

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from playwright.async_api import async_playwright
from scripts.generate_voice import synthesize

SOURCE = "https://www.dawateislami.net/hadees/ur/books/muntakhab-hadeesen/hadees-1"
OUT = Path("output")
OUT.mkdir(exist_ok=True)
W, H, FPS = 1920, 1080, 30
DURATION = 90

async def fetch_page_text() -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(SOURCE, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(1200)
        text = await page.locator("body").inner_text()
        await browser.close()
        return text

plain = asyncio.run(fetch_page_text())
if "منتخب حدیثیں" not in plain or "حدیث نمبر: 1" not in plain:
    raise SystemExit("Official Dawat-e-Islami Hadith #1 source could not be verified.")

def section(text: str, start: str, end: str) -> str:
    if start not in text or end not in text:
        raise SystemExit(f"Official source section missing: {start}")
    value = text.split(start, 1)[1].split(end, 1)[0]
    return re.sub(r"\n{2,}", "\n", value).strip()

arabic_block = section(plain, "حدیث مبارکہ", "حدیث ترجمہ")
translation = section(plain, "حدیث ترجمہ", "شرح حدیث")
arabic_block = re.sub(r"^.*?حدیث مبارکہ\s*", "", arabic_block, flags=re.S).strip()
translation = translation.strip()
if len(arabic_block) < 80 or len(translation) < 80:
    raise SystemExit("Official Hadith text extraction was unexpectedly short.")

voice = OUT / "hadith-001-voice.mp3"
synthesize(translation, str(voice))

metadata = f"""source: {SOURCE}
source_policy: Dawat-e-Islami official website only
hadith_number: 1
book_reference: منتخب حدیثیں، جلد 1
format: 1920x1080 16:9
duration_target_seconds: {DURATION}
fps: {FPS}
status: REVIEW_REQUIRED
youtube_publish: OFF
human_approval: REQUIRED
"""
(OUT / "hadith-001-source.txt").write_text(metadata, encoding="utf-8")

def make_slide(name: str, heading: str, body: str, footer: str) -> Path:
    safe_heading, safe_body, safe_footer = map(escape, (heading, body, footer))
    html = f"""<!doctype html><meta charset="utf-8">
<style>
@font-face{{font-family:Nastaliq;src:local("Noto Nastaliq Urdu")}}
html,body{{margin:0;width:1920px;height:1080px;background:#07140d;color:#fff}}
body{{font-family:Nastaliq,serif}}
main{{height:100%;box-sizing:border-box;padding:90px 150px;display:flex;flex-direction:column;justify-content:center;text-align:center}}
h1{{font-size:70px;color:#d4af37;margin:0 0 35px}}
p{{font-size:46px;line-height:2;margin:0 auto;max-width:1550px;white-space:pre-wrap}}
footer{{font-family:Arial,sans-serif;font-size:24px;margin-top:45px;opacity:.85}}
</style><main><h1>{safe_heading}</h1><p>{safe_body}</p><footer>{safe_footer}</footer></main>"""
    path = OUT / f"{name}.html"
    path.write_text(html, encoding="utf-8")
    return path

slides = [
    ("slide01", "حدیثِ مبارک", "نیت کی اہمیت", "Hidayat Tube Official"),
    ("slide02", "حدیثِ مبارک", arabic_block, "Official Dawat-e-Islami source"),
    ("slide03", "حدیثِ مبارک", translation, "Official Urdu translation"),
    ("slide04", "حوالہ", "حدیث نمبر: 1\nبک ریفرنس: منتخب حدیثیں، جلد 1", "Hidayat Tube Official"),
]

async def render_slides():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for name, heading, body, footer in slides:
            path = make_slide(name, heading, body, footer)
            await page.goto(path.resolve().as_uri(), wait_until="load")
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(300)
            await page.screenshot(path=str(OUT / f"{name}.png"))
        await browser.close()

asyncio.run(render_slides())

durations = [6, 22, 55, 7]
inputs = []
for i, (name, *_rest) in enumerate(slides):
    inputs += ["-loop", "1", "-t", str(durations[i]), "-i", str(OUT / f"{name}.png")]

filters = []
for i in range(len(slides)):
    filters.append(f"[{i}:v]fps={FPS},format=yuv420p,setsar=1[v{i}]")
filters.append("[v0][v1]xfade=transition=fade:duration=1:offset=5[v01]")
filters.append("[v01][v2]xfade=transition=fade:duration=1:offset=26[v012]")
filters.append("[v012][v3]xfade=transition=fade:duration=1:offset=80[v]")
silent = OUT / "hadith-001-silent.mp4"
subprocess.run([
    "ffmpeg","-y",*inputs,"-filter_complex",";".join(filters),
    "-map","[v]","-t",str(DURATION),"-c:v","libx264","-pix_fmt","yuv420p",
    "-r",str(FPS),"-movflags","+faststart",str(silent)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

video = OUT / "hadith-001-review.mp4"
subprocess.run([
    "ffmpeg","-y","-i",str(silent),"-i",str(voice),
    "-map","0:v:0","-map","1:a:0","-t",str(DURATION),
    "-c:v","libx264","-pix_fmt","yuv420p","-r",str(FPS),
    "-c:a","aac","-ar","44100","-ac","2","-b:a","128k",
    "-af",f"apad=pad_dur={DURATION}","-movflags","+faststart",str(video)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

probe = subprocess.run([
    "ffprobe","-v","error","-show_entries",
    "format=format_name,duration:stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate",
    "-of","default=noprint_wrappers=1",str(video)
], check=True, capture_output=True, text=True).stdout
for required in ("codec_name=h264","codec_name=aac","width=1920","height=1080","pix_fmt=yuv420p"):
    if required not in probe:
        raise SystemExit(f"MP4 validation failed: {required}")
print(probe)

for p in OUT.glob("slide*.png"): p.unlink(missing_ok=True)
for p in OUT.glob("slide*.html"): p.unlink(missing_ok=True)
silent.unlink(missing_ok=True)
print(f"Verified Hadith #001 long-form review: {video}")
