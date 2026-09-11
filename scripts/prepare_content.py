"""Prepare a YouTube-compatible Urdu Islamic reminder video for private review."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess

import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

OUT = Path("output")
OUT.mkdir(exist_ok=True)

TOPIC = "روزانہ اسلامی یاددہانی"
SCENES = [
    "السلام علیکم ورحمۃ اللہ وبرکاتہ۔\nآج کا مختصر اسلامی پیغام",
    "نیکی کے چھوٹے اعمال کو معمولی نہ سمجھیں۔\nاللہ کی رضا کے لیے کیا گیا نیک عمل بہت قیمتی ہے۔",
    "آج ایک نیکی کا ارادہ کریں،\nاخلاص کے ساتھ عمل کریں اور دوسروں کے لیے آسانی پیدا کریں۔",
    "ایسی مختصر اسلامی یاددہانیاں روزانہ پانے کے لیے\nچینل کو سبسکرائب کریں اور یہ پیغام کسی اپنے تک پہنچائیں۔",
]
VOICE_TEXT = (
    "السلام علیکم ورحمۃ اللہ وبرکاتہ۔ آج کا مختصر اسلامی پیغام۔ "
    "نیکی کے چھوٹے اعمال کو معمولی نہ سمجھیں۔ اللہ کی رضا کے لیے کیا گیا نیک عمل بہت قیمتی ہے۔ "
    "آج ایک نیکی کا ارادہ کریں، اخلاص کے ساتھ عمل کریں اور دوسروں کے لیے آسانی پیدا کریں۔ "
    "ایسی مختصر اسلامی یاددہانیاں روزانہ پانے کے لیے چینل کو سبسکرائب کریں اور یہ پیغام کسی اپنے تک پہنچائیں۔"
)

SCRIPT = f"""# {TOPIC}\n\n{VOICE_TEXT}\n\nنوٹ: اشاعت سے پہلے قرآن و حدیث کے اصل حوالہ جات مستند ذریعے سے انسانی طور پر verify کیے جائیں۔\n"""
metadata = f"""topic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\nduration_target_seconds: 30\nvoice: Urdu TTS\nvideo_codec: H.264\naudio_codec: AAC\nsubscriber_cta: enabled\nstatus: REVIEW_REQUIRED\n"""
(OUT / "script.md").write_text(SCRIPT, encoding="utf-8")
(OUT / "metadata.txt").write_text(metadata, encoding="utf-8")

font_path = "/usr/share/fonts/truetype/noto/NotoNastaliqUrdu-Regular.ttf"
font = ImageFont.truetype(font_path, 54)
small = ImageFont.truetype(font_path, 38)


def rtl(text: str) -> str:
    return get_display(arabic_reshaper.reshape(text))


def make_scene(text: str, path: Path, number: int) -> None:
    img = Image.new("RGB", (1280, 720), "black")
    draw = ImageDraw.Draw(img)
    draw.multiline_text((640, 120), rtl(TOPIC), font=font, fill="white", anchor="ma", align="center", spacing=18)
    body = "\n".join(rtl(line) for line in text.splitlines())
    draw.multiline_text((640, 295), body, font=small, fill="white", anchor="ma", align="center", spacing=24)
    draw.text((640, 625), rtl(f"منظر {number} • جائزہ ضروری ہے"), font=small, fill="white", anchor="mm")
    img.save(path, format="PNG")

scenes = []
for index, text in enumerate(SCENES, start=1):
    path = OUT / f"scene_{index}.png"
    make_scene(text, path, index)
    scenes.append(path)

concat = OUT / "scenes.txt"
concat.write_text(
    "".join(f"file '{p.name}'\nduration 7.5\n" for p in scenes) + f"file '{scenes[-1].name}'\n",
    encoding="utf-8",
)

silent = OUT / "silent.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
    "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2",
    "-t", "30", "-r", "30", "-pix_fmt", "yuv420p", "-c:v", "libx264",
    "-profile:v", "high", "-level", "4.0", "-movflags", "+faststart", str(silent)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

voice = OUT / "voice.wav"
subprocess.run([
    "espeak-ng", "-v", "ur", "-s", "145", "-p", "45", "-w", str(voice), VOICE_TEXT
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

video = OUT / "video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(silent), "-i", str(voice),
    "-map", "0:v:0", "-map", "1:a:0", "-t", "30",
    "-c:v", "libx264", "-profile:v", "high", "-level", "4.0",
    "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-ar", "48000",
    "-ac", "2", "-b:a", "128k", "-movflags", "+faststart", str(video)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

probe = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name",
    "-of", "default=noprint_wrappers=1", str(video)
], check=True, capture_output=True, text=True)
print(probe.stdout)
if "codec_type=video" not in probe.stdout or "codec_type=audio" not in probe.stdout:
    raise SystemExit("Generated MP4 is missing video or audio stream")

for path in scenes + [concat, silent, voice]:
    path.unlink(missing_ok=True)

print(f"Verified YouTube-compatible Urdu review video: {video}")
