"""Render a professional vertical Urdu Islamic reminder video for private review."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess

import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

OUT = Path("output")
OUT.mkdir(exist_ok=True)

W, H = 1080, 1920
FPS = 30
SCENE_SECONDS = 7.5
TOPIC = "روزانہ اسلامی یاددہانی"
SCENES = [
    "السلام علیکم ورحمۃ اللہ وبرکاتہ۔\nآج کا مختصر اسلامی پیغام",
    "نیکی کے چھوٹے اعمال کو معمولی نہ سمجھیں۔\nاللہ کی رضا کے لیے کیا گیا نیک عمل بہت قیمتی ہے۔",
    "آج ایک نیکی کا ارادہ کریں،\nاخلاص کے ساتھ عمل کریں اور دوسروں کے لیے آسانی پیدا کریں۔",
    "اگر یہ پیغام مفید لگا تو Like کریں۔\nروزانہ اسلامی یاددہانیوں کے لیے Subscribe کریں۔\nاور یہ پیغام کسی اپنے تک Share کریں۔",
]
VOICE_TEXT = (
    "السلام علیکم ورحمۃ اللہ وبرکاتہ۔ آج کا مختصر اسلامی پیغام۔ "
    "نیکی کے چھوٹے اعمال کو معمولی نہ سمجھیں۔ اللہ کی رضا کے لیے کیا گیا نیک عمل بہت قیمتی ہے۔ "
    "آج ایک نیکی کا ارادہ کریں، اخلاص کے ساتھ عمل کریں اور دوسروں کے لیے آسانی پیدا کریں۔ "
    "اگر یہ پیغام مفید لگا تو لائک کریں۔ روزانہ اسلامی یاددہانیوں کے لیے چینل کو سبسکرائب کریں۔ اور یہ پیغام کسی اپنے تک شیئر کریں۔"
)

SCRIPT = f"""# {TOPIC}\n\n{VOICE_TEXT}\n\nنوٹ: اشاعت سے پہلے قرآن و حدیث کے اصل حوالہ جات مستند ذریعے سے انسانی طور پر verify کیے جائیں۔\n"""
metadata = f"""topic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\nduration_target_seconds: 30\nformat: YouTube Shorts 9:16\nresolution: 1080x1920\nframe_rate: 30\nvoice: Urdu TTS\nvideo_codec: H.264 Baseline\naudio_codec: AAC-LC\nsubscriber_cta: enabled\nlike_cta: enabled\nshare_cta: enabled\nvisual_style: professional dark-gold Islamic card design\nstatus: REVIEW_REQUIRED\n"""
(OUT / "script.md").write_text(SCRIPT, encoding="utf-8")
(OUT / "metadata.txt").write_text(metadata, encoding="utf-8")

font_path = "/usr/share/fonts/truetype/amiri/Amiri-Regular.ttf"
font_bold_path = "/usr/share/fonts/truetype/amiri/Amiri-Bold.ttf"
font = ImageFont.truetype(font_bold_path if Path(font_bold_path).exists() else font_path, 70)
body_font = ImageFont.truetype(font_path, 52)
small = ImageFont.truetype(font_path, 34)


def rtl(text: str) -> str:
    return get_display(arabic_reshaper.reshape(text))


def gradient_background() -> Image.Image:
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        r = int(8 + 12 * t)
        g = int(13 + 10 * t)
        b = int(24 + 15 * t)
        for x in range(W):
            glow = int(10 * max(0, 1 - (((x - W * 0.5) / (W * 0.7)) ** 2)))
            px[x, y] = (min(35, r + glow), min(38, g + glow), min(55, b + glow))
    return img


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, start: int, minimum: int = 34):
    size = start
    while size > minimum:
        f = ImageFont.truetype(font_path, size)
        bbox = draw.multiline_textbbox((0, 0), text, font=f, spacing=18, align="center")
        if bbox[2] - bbox[0] <= max_width:
            return f
        size -= 2
    return ImageFont.truetype(font_path, minimum)


def make_scene(text: str, path: Path, number: int) -> None:
    img = gradient_background()
    draw = ImageDraw.Draw(img)

    # Decorative border and top label.
    draw.rounded_rectangle((42, 42, W - 42, H - 42), radius=34, outline=(150, 125, 60), width=3)
    draw.rounded_rectangle((170, 130, W - 170, 260), radius=45, fill=(22, 29, 45), outline=(150, 125, 60), width=2)
    draw.text((W // 2, 195), rtl(TOPIC), font=font, fill=(245, 235, 200), anchor="mm")

    # Main content card: deliberately large, high-contrast and free of cramped text.
    card = (90, 480, W - 90, 1375)
    draw.rounded_rectangle(card, radius=58, fill=(18, 25, 40), outline=(150, 125, 60), width=3)
    draw.rounded_rectangle((125, 515, W - 125, 550), radius=17, fill=(150, 125, 60))

    lines = []
    for line in text.splitlines():
        lines.append(rtl(line))
    body = "\n".join(lines)
    body_font_fit = fit_text(draw, body, 820, 52)
    draw.multiline_text((W // 2, 920), body, font=body_font_fit, fill=(250, 250, 248), anchor="mm", align="center", spacing=30)

    # Bottom review badge and scene counter.
    draw.rounded_rectangle((210, 1500, W - 210, 1605), radius=38, fill=(24, 32, 48), outline=(150, 125, 60), width=2)
    draw.text((W // 2, 1552), rtl(f"منظر {number} • جائزہ ضروری ہے"), font=small, fill=(225, 215, 185), anchor="mm")
    draw.text((W // 2, 1760), "HIDAYAT TUBE", font=ImageFont.truetype(font_path, 30), fill=(170, 170, 175), anchor="mm")
    img.save(path, format="PNG", optimize=True)


scenes = []
for index, text in enumerate(SCENES, start=1):
    path = OUT / f"scene_{index}.png"
    make_scene(text, path, index)
    scenes.append(path)

# Build a clean 30-second video with smooth crossfades between professional title cards.
inputs = []
for scene in scenes:
    inputs += ["-loop", "1", "-t", str(SCENE_SECONDS), "-i", str(scene)]

filter_parts = []
for i in range(len(scenes)):
    filter_parts.append(f"[{i}:v]fps={FPS},format=yuv420p,setsar=1[v{i}]")
current = "v0"
current_duration = SCENE_SECONDS
for i in range(1, len(scenes)):
    out = f"xf{i}"
    offset = current_duration - 0.55
    filter_parts.append(f"[{current}][v{i}]xfade=transition=fade:duration=0.55:offset={offset:.2f}[{out}]")
    current = out
    current_duration += SCENE_SECONDS - 0.55

silent = OUT / "silent.mp4"
subprocess.run([
    "ffmpeg", "-y", *inputs,
    "-filter_complex", ";".join(filter_parts),
    "-map", f"[{current}]", "-t", "30",
    "-c:v", "libx264", "-profile:v", "baseline", "-level", "4.0",
    "-pix_fmt", "yuv420p", "-r", str(FPS), "-fps_mode", "cfr",
    "-preset", "medium", "-movflags", "+faststart", str(silent)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

voice = OUT / "voice.wav"
subprocess.run([
    "espeak-ng", "-v", "ur", "-s", "145", "-p", "45", "-w", str(voice), VOICE_TEXT
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

video = OUT / "video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(silent), "-i", str(voice),
    "-map", "0:v:0", "-map", "1:a:0", "-t", "30",
    "-c:v", "libx264", "-profile:v", "baseline", "-level", "4.0",
    "-pix_fmt", "yuv420p", "-r", str(FPS), "-fps_mode", "cfr",
    "-c:a", "aac", "-profile:a", "aac_low", "-ar", "44100",
    "-ac", "2", "-b:a", "128k", "-af", ""apad=pad_dur=30"",
    "-movflags", "+faststart", str(video)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

probe = subprocess.run([
    "ffprobe", "-v", "error",
    "-show_entries", "format=format_name,duration:stream=index,codec_type,codec_name,profile,pix_fmt,r_frame_rate,sample_rate,channels,width,height",
    "-of", "default=noprint_wrappers=1", str(video)
], check=True, capture_output=True, text=True)
print(probe.stdout)
required = [
    "codec_type=video", "codec_name=h264", "pix_fmt=yuv420p",
    "codec_type=audio", "codec_name=aac", "width=1080", "height=1920",
]
if any(item not in probe.stdout for item in required):
    raise SystemExit("Generated professional MP4 failed stream/resolution checks")
if "format_name=mov,mp4,m4a,3gp,3g2,mj2" not in probe.stdout:
    raise SystemExit("Generated file is not a standard MP4 container")

# Full decode test: do not upload a file that FFmpeg cannot read end-to-end.
subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], check=True)

for path in scenes + [silent, voice]:
    path.unlink(missing_ok=True)

print(f"Verified professional 1080x1920 H.264/AAC MP4 with full decode: {video}")
