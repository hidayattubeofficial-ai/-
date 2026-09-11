"""Render a professional vertical Urdu Islamic reminder video for private review."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess

from PIL import Image, ImageDraw

OUT = Path("output")
OUT.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 30
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
SCRIPT = f"# {TOPIC}\n\n{VOICE_TEXT}\n\nنوٹ: اشاعت سے پہلے قرآن و حدیث کے اصل حوالہ جات مستند ذریعے سے انسانی طور پر verify کیے جائیں۔\n"
metadata = f"topic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\nduration_target_seconds: 30\nformat: YouTube Shorts 9:16\nresolution: 1080x1920\nframe_rate: 30\nvoice: Urdu TTS\nvideo_codec: H.264 Baseline\naudio_codec: AAC-LC\nsubscriber_cta: enabled\nlike_cta: enabled\nshare_cta: enabled\nvisual_style: professional dark-gold Islamic card design\nfont: Noto Nastaliq Urdu via Chromium Playwright\ntext_renderer: Chromium RTL/complex-text shaping\nstatus: REVIEW_REQUIRED\n"
(OUT / "script.md").write_text(SCRIPT, encoding="utf-8")
(OUT / "metadata.txt").write_text(metadata, encoding="utf-8")


def gradient_background() -> Image.Image:
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        base = (8 + int(12*t), 13 + int(10*t), 24 + int(15*t))
        for x in range(W):
            glow = int(10 * max(0, 1 - (((x - W*0.5)/(W*0.7))**2)))
            px[x, y] = (min(35, base[0]+glow), min(38, base[1]+glow), min(55, base[2]+glow))
    return img


def make_background(path: Path) -> None:
    img = gradient_background()
    draw = ImageDraw.Draw(img)
    gold = (150, 125, 60)
    draw.rounded_rectangle((42,42,W-42,H-42), radius=34, outline=gold, width=3)
    draw.rounded_rectangle((170,130,W-170,260), radius=45, fill=(22,29,45), outline=gold, width=2)
    draw.rounded_rectangle((90,480,W-90,1375), radius=58, fill=(18,25,40), outline=gold, width=3)
    draw.rounded_rectangle((125,515,W-125,550), radius=17, fill=gold)
    draw.rounded_rectangle((210,1500,W-210,1605), radius=38, fill=(24,32,48), outline=gold, width=2)
    draw.text((W//2,1760), "HIDAYAT TUBE", fill=(170,170,175), anchor="mm")
    img.save(path, format="PNG", optimize=True)


def run_renderer(title: str, body: str, footer: str, output: Path) -> None:
    subprocess.run([
        "python", "scripts/render_text.py", title, body, footer, str(output)
    ], check=True)


scene_videos = []
for i, text in enumerate(SCENES, 1):
    bg = OUT / f"scene_{i}_background.png"
    overlay = OUT / f"scene_{i}_text.png"
    scene_video = OUT / f"scene_{i}.mp4"
    make_background(bg)
    run_renderer(TOPIC, text, f"منظر {i} • جائزہ ضروری ہے", overlay)
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(bg), "-loop", "1", "-i", str(overlay),
        "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p,setsar=1",
        "-t", str(SCENE_SECONDS), "-r", str(FPS), "-c:v", "libx264", "-profile:v", "baseline",
        "-level", "4.0", "-pix_fmt", "yuv420p", "-an", str(scene_video)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    scene_videos.append(scene_video)

inputs = []
for scene in scene_videos:
    inputs += ["-i", str(scene)]
filters = [f"[{i}:v]fps={FPS},format=yuv420p,setsar=1[v{i}]" for i in range(len(scene_videos))]
current = "v0"
current_duration = SCENE_SECONDS
for i in range(1, len(scene_videos)):
    out = f"xf{i}"
    offset = current_duration - 0.55
    filters.append(f"[{current}][v{i}]xfade=transition=fade:duration=0.55:offset={offset:.2f}[{out}]")
    current = out
    current_duration += SCENE_SECONDS - 0.55

silent = OUT / "silent.mp4"
subprocess.run([
    "ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filters),
    "-map", f"[{current}]", "-t", "30", "-c:v", "libx264", "-profile:v", "baseline",
    "-level", "4.0", "-pix_fmt", "yuv420p", "-r", str(FPS), "-fps_mode", "cfr",
    "-preset", "medium", "-movflags", "+faststart", str(silent)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

voice = OUT / "voice.wav"
subprocess.run(["espeak-ng", "-v", "ur", "-s", "145", "-p", "45", "-w", str(voice), VOICE_TEXT], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

video = OUT / "video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(silent), "-i", str(voice), "-map", "0:v:0", "-map", "1:a:0", "-t", "30",
    "-c:v", "libx264", "-profile:v", "baseline", "-level", "4.0", "-pix_fmt", "yuv420p",
    "-r", str(FPS), "-fps_mode", "cfr", "-c:a", "aac", "-profile:a", "aac_low", "-ar", "44100",
    "-ac", "2", "-b:a", "128k", "-af", "apad=pad_dur=30", "-movflags", "+faststart", str(video)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

probe = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries",
    "format=format_name,duration:stream=index,codec_type,codec_name,profile,pix_fmt,r_frame_rate,sample_rate,channels,width,height",
    "-of", "default=noprint_wrappers=1", str(video)
], check=True, capture_output=True, text=True)
print(probe.stdout)
required = ["codec_type=video", "codec_name=h264", "pix_fmt=yuv420p", "codec_type=audio", "codec_name=aac", "width=1080", "height=1920"]
if any(x not in probe.stdout for x in required):
    raise SystemExit("Generated professional MP4 failed stream/resolution checks")
if "format_name=mov,mp4,m4a,3gp,3g2,mj2" not in probe.stdout:
    raise SystemExit("Generated file is not a standard MP4 container")
subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], check=True)
for path in scene_videos:
    path.unlink(missing_ok=True)
for path in OUT.glob("scene_*_background.png"):
    path.unlink(missing_ok=True)
for path in OUT.glob("scene_*_text.png"):
    path.unlink(missing_ok=True)
silent.unlink(missing_ok=True)
voice.unlink(missing_ok=True)
print(f"Verified professional 1080x1920 H.264/AAC MP4 with full decode: {video}")
