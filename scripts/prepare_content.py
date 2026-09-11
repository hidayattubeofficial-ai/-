"""Prepare reviewable content and a simple MP4 for the private YouTube workflow."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess

from PIL import Image, ImageDraw, ImageFont

OUT = Path("output")
OUT.mkdir(exist_ok=True)

TOPIC = "Daily Islamic Reminder"
MESSAGE = "نیکی کے چھوٹے کاموں کو معمولی نہ سمجھیں۔\nاخلاص کے ساتھ کیا گیا اچھا عمل برکت کا ذریعہ بن سکتا ہے۔"

SCRIPT = f"""# {TOPIC}\n\nالسلام علیکم ورحمۃ اللہ وبرکاتہ۔\n\nآج کا مختصر اسلامی پیغام: {MESSAGE.replace(chr(10), ' ')}\n\nاپنے دن میں ایک نیکی کا انتخاب کریں، اسے اخلاص کے ساتھ کریں، اور دوسروں کے لیے بھی آسانی پیدا کریں۔\n\nنوٹ: اشاعت سے پہلے قرآن و حدیث کے اصل حوالہ جات مستند ذریعے سے انسانی طور پر verify کیے جائیں۔\n"""

metadata = f"""topic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\nstatus: REVIEW_REQUIRED\n"""

(OUT / "script.md").write_text(SCRIPT, encoding="utf-8")
(OUT / "metadata.txt").write_text(metadata, encoding="utf-8")

# Generate a short, silent review video. It is uploaded as PRIVATE only.
img = Image.new("RGB", (1280, 720), "black")
draw = ImageDraw.Draw(img)
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font = ImageFont.truetype(font_path, 42)
small = ImageFont.truetype(font_path, 30)

def center(text: str, y: int, fnt: ImageFont.FreeTypeFont) -> None:
    box = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=14, align="center")
    x = (1280 - (box[2] - box[0])) // 2
    draw.multiline_text((x, y), text, font=fnt, fill="white", spacing=14, align="center")

center(TOPIC, 170, font)
center("Daily Islamic Reminder", 270, small)
center("REVIEW REQUIRED", 500, small)
frame = OUT / "frame.png"
img.save(frame)

video = OUT / "video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-loop", "1", "-i", str(frame),
    "-t", "10", "-r", "30", "-pix_fmt", "yuv420p",
    "-c:v", "libx264", "-movflags", "+faststart", str(video)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

frame.unlink(missing_ok=True)
print(f"Content package and review video prepared: {video}")
