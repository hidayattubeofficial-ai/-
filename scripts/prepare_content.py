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
    "اگر یہ پیغام مفید لگا تو Like کریں۔\nروزانہ اسلامی یاددہانیوں کے لیے Subscribe کریں۔\nاور یہ پیغام کسی اپنے تک Share کریں۔",
]
VOICE_TEXT = (
    "السلام علیکم ورحمۃ اللہ وبرکاتہ۔ آج کا مختصر اسلامی پیغام۔ "
    "نیکی کے چھوٹے اعمال کو معمولی نہ سمجھیں۔ اللہ کی رضا کے لیے کیا گیا نیک عمل بہت قیمتی ہے۔ "
    "آج ایک نیکی کا ارادہ کریں، اخلاص کے ساتھ عمل کریں اور دوسروں کے لیے آسانی پیدا کریں۔ "
    "اگر یہ پیغام مفید لگا تو لائک کریں۔ روزانہ اسلامی یاددہانیوں کے لیے چینل کو سبسکرائب کریں۔ اور یہ پیغام کسی اپنے تک شیئر کریں۔"
)

SCRIPT = f"""# {TOPIC}\n\n{VOICE_TEXT}\n\nنوٹ: اشاعت سے پہلے قرآن و حدیث کے اصل حوالہ جات مستند ذریعے سے انسانی طور پر verify کیے جائیں۔\n"""
metadata = f"""topic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\nduration_target_seconds: 30\nvoice: Urdu TTS\nvideo_codec: H.264\naudio_codec: AAC\nsubscriber_cta: enabled\nlike_cta: enabled\nshare_cta: enabled\nstatus: REVIEW_REQUIRED\n"""
(OUT / "script.md").write_text(SCRIPT, encoding="utf-8")
(OUT / "metadata.txt").write_text(metadata, encoding="utf-8")

# Use Amiri for reliable Urdu/Arabic glyph coverage in GitHub's Linux runner.
font_path = "/usr/share/fonts/truetype/amiri/Amiri-Regular.ttf"
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
    "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
    "-t", "30", "-r", "30", "-fps_mode", "cfr", "-pix_fmt", "yuv420p",
    "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.1",
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
    "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.1",
    "-pix_fmt", "yuv420p", "-r", "30", "-fps_mode", "cfr",
    "-c:a", "aac", "-profile:a", "aac_low", "-ar", "44100",
    "-ac", "2", "-b:a", "128k", "-movflags", "+faststart", str(video)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

probe = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "format=format_name,duration:stream=index,codec_type,codec_name,profile,pix_fmt,r_frame_rate,sample_rate,channels",
    "-of", "default=noprint_wrappers=1", str(video)
], check=True, capture_output=True, text=True)
print(probe.stdout)
required = ["codec_type=video", "codec_name=h264", "codec_type=audio", "codec_name=aac", "pix_fmt=yuv420p"]
if any(item not in probe.stdout for item in required):
    raise SystemExit("Generated MP4 failed compatibility stream checks")
if "format_name=mov,mp4,m4a,3gp,3g2,mj2" not in probe.stdout:
    raise SystemExit("Generated file is not a standard MP4 container")

# Decode the entire MP4 before uploading; metadata-only checks are not enough.
subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], check=True)

for path in scenes + [concat, silent, voice]:
    path.unlink(missing_ok=True)

print(f"Verified maximum-compatibility YouTube MP4 with full decode: {video}")
