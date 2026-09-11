"""Prepare a playable Urdu Islamic reminder video for private review."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess

import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

OUT = Path("output")
OUT.mkdir(exist_ok=True)

TOPIC = "Daily Islamic Reminder"
SCENES = [
    "السلام علیکم ورحمۃ اللہ وبرکاتہ۔\nآج کا مختصر اسلامی پیغام",
    "نیکی کے چھوٹے کاموں کو معمولی نہ سمجھیں۔\nاخلاص کے ساتھ کیا گیا اچھا عمل برکت کا ذریعہ بن سکتا ہے۔",
    "اپنے دن میں ایک نیکی کا انتخاب کریں،\nاسے اخلاص کے ساتھ کریں، اور دوسروں کے لیے آسانی پیدا کریں۔",
]
VOICE_TEXT = (
    "السلام علیکم ورحمۃ اللہ وبرکاتہ۔ آج کا مختصر اسلامی پیغام۔ "
    "نیکی کے چھوٹے کاموں کو معمولی نہ سمجھیں۔ اخلاص کے ساتھ کیا گیا اچھا عمل برکت کا ذریعہ بن سکتا ہے۔ "
    "اپنے دن میں ایک نیکی کا انتخاب کریں، اسے اخلاص کے ساتھ کریں، اور دوسروں کے لیے آسانی پیدا کریں۔"
)

SCRIPT = f"""# {TOPIC}\n\n{VOICE_TEXT}\n\nنوٹ: اشاعت سے پہلے قرآن و حدیث کے اصل حوالہ جات مستند ذریعے سے انسانی طور پر verify کیے جائیں۔\n"""
metadata = f"""topic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\nduration_target_seconds: 30\nvoice: Urdu TTS\nstatus: REVIEW_REQUIRED\n"""
(OUT / "script.md").write_text(SCRIPT, encoding="utf-8")
(OUT / "metadata.txt").write_text(metadata, encoding="utf-8")

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font = ImageFont.truetype(font_path, 42)
small = ImageFont.truetype(font_path, 28)


def rtl(text: str) -> str:
    return get_display(arabic_reshaper.reshape(text))


def make_scene(text: str, path: Path, number: int) -> None:
    img = Image.new("RGB", (1280, 720), "black")
    draw = ImageDraw.Draw(img)
    title = rtl(TOPIC)
    body = "\n".join(rtl(line) for line in text.splitlines())
    draw.multiline_text((640, 145), title, font=font, fill="white", anchor="ma", align="center", spacing=16)
    draw.multiline_text((640, 285), body, font=small, fill="white", anchor="ma", align="center", spacing=18)
    draw.text((640, 620), f"Scene {number} • REVIEW REQUIRED", font=small, fill="white", anchor="mm")
    img.save(path)

scenes = []
for index, text in enumerate(SCENES, start=1):
    path = OUT / f"scene_{index}.png"
    make_scene(text, path, index)
    scenes.append(path)

concat = OUT / "scenes.txt"
concat.write_text(
    "".join(f"file '{p.name}'\nduration 10\n" for p in scenes) + f"file '{scenes[-1].name}'\n",
    encoding="utf-8",
)

silent = OUT / "silent.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
    "-vf", "scale=1280:720", "-r", "30", "-pix_fmt", "yuv420p",
    "-c:v", "libx264", "-movflags", "+faststart", str(silent)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

voice = OUT / "voice.wav"
subprocess.run([
    "espeak-ng", "-v", "ur", "-s", "145", "-p", "45", "-w", str(voice), VOICE_TEXT
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

video = OUT / "video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(silent), "-i", str(voice),
    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
    "-b:a", "128k", "-shortest", "-movflags", "+faststart", str(video)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

for path in scenes + [concat, silent, voice]:
    path.unlink(missing_ok=True)

print(f"Playable Islamic review video prepared: {video}")
