"""Render a professional vertical Urdu Islamic reminder video for private review."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess

from PIL import Image, ImageDraw
from scripts.generate_voice import synthesize

OUT = Path("output")
OUT.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 30
SCENE_SECONDS = 7.5
XFADE_SECONDS = 0.55
TOPIC = "روزانہ اسلامی یاددہانی"
BRANDING_DIR = Path("assets/branding")
BRANDING_BG = BRANDING_DIR / "bg.png"
SCENES = [
    "السلام علیکم ورحمۃ اللہ وبرکاتہ۔\nآج کا مختصر اسلامی پیغام",
    "نیکی کے چھوٹے اعمال کو معمولی نہ سمجھیں۔\nاللہ کی رضا کے لیے کیا گیا نیک عمل بہت قیمتی ہے۔",
    "آج ایک نیکی کا ارادہ کریں،\nاخلاص کے ساتھ عمل کریں اور دوسروں کے لیے آسانی پیدا کریں۔",
    "اگر یہ پیغام مفید لگا تو Like کریں۔\n\nاور یہ پیغام کسی اپنے تک Share کریں۔",
]
VOICE_TEXT = (
    "السلام علیکم ورحمۃ اللہ وبرکاتہ۔ آج کا مختصر اسلامی پیغام۔ "
    "نیکی کے چھوٹے اعمال کو معمولی نہ سمجھیں۔ اللہ کی رضا کے لیے کیا گیا نیک عمل بہت قیمتی ہے۔ "
    "آج ایک نیکی کا ارادہ کریں، اخلاص کے ساتھ عمل کریں اور دوسروں کے لیے آسانی پیدا کریں۔ "
    "اگر یہ پیغام مفید لگا تو لائک کریں۔ روزانہ اسلامی یاددہانیوں کے لیے چینل کو سبسکرائب کریں۔ اور یہ پیغام کسی اپنے تک شیئر کریں۔"
)
SCRIPT = f"# {TOPIC}\n\n{VOICE_TEXT}\n\nنوٹ: اشاعت سے پہلے قرآن و حدیث کے اصل حوالہ جات مستند ذریعے سے انسانی طور پر verify کیے جائیں۔\n"
metadata = f"topic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\nduration_target_seconds: 30\nformat: YouTube Shorts 9:16\nresolution: 1080x1920\nframe_rate: 30\nvoice: Microsoft Edge Neural Urdu ({__import__('os').getenv('TTS_VOICE', 'ur-PK-AsadNeural')})\nvideo_codec: H.264 Baseline\naudio_codec: AAC-LC\nsubscriber_cta: enabled\nlike_cta: enabled\nshare_cta: enabled\nvisual_style: Hidayat Tube full black-and-gold branding background\nfont: Noto Nastaliq Urdu via Chromium Playwright\ntext_renderer: Chromium RTL/complex-text shaping\nstatus: REVIEW_REQUIRED\n"
(OUT / "script.md").write_text(SCRIPT, encoding="utf-8")
(OUT / "metadata.txt").write_text(metadata, encoding="utf-8")


def _cover_resize(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize/crop a supplied branding image to the exact Shorts canvas."""
    img = img.convert("RGB")
    scale = max(size[0] / img.width, size[1] / img.height)
    resized = img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - size[0]) // 2)
    top = max(0, (resized.height - size[1]) // 2)
    return resized.crop((left, top, left + size[0], top + size[1]))


def make_background(path: Path) -> None:
    # Use the channel's supplied branding artwork as the actual scene background.
    # This is intentionally different from the old generic gradient card: the
    # branded artwork is now visible throughout the video, while the Chromium
    # layer adds the readable Urdu title/body/footer on top.
    if not BRANDING_BG.exists():
        raise FileNotFoundError(f"Required Hidayat Tube branding background is missing: {BRANDING_BG}")

    img = _cover_resize(Image.open(BRANDING_BG), (W, H))
    draw = ImageDraw.Draw(img, "RGBA")

    # Preserve the supplied artwork but add a restrained translucent reading area
    # so the Nastaliq message remains legible without replacing the branding.
    draw.rounded_rectangle((70, 455, W - 70, 1420), radius=58,
                           fill=(8, 12, 24, 118), outline=(190, 155, 70, 190), width=3)
    draw.rounded_rectangle((108, 492, W - 108, 535), radius=18,
                           fill=(190, 155, 70, 215))
    img.save(path, format="PNG", optimize=True)


def run_renderer(title: str, body: str, footer: str, output: Path) -> None:
    subprocess.run([
        "python", "scripts/render_text.py", title, body, footer, str(output)
    ], check=True)


def run_cta_renderer(output: Path) -> None:
    subprocess.run([
        "python", "scripts/render_text.py", "--cta", str(output)
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
    offset = current_duration - XFADE_SECONDS
    filters.append(f"[{current}][v{i}]xfade=transition=fade:duration={XFADE_SECONDS}:offset={offset:.2f}[{out}]")
    current = out
    current_duration += SCENE_SECONDS - XFADE_SECONDS

silent = OUT / "silent.mp4"
subprocess.run([
    "ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filters),
    "-map", f"[{current}]", "-t", "30", "-c:v", "libx264", "-profile:v", "baseline",
    "-level", "4.0", "-pix_fmt", "yuv420p", "-r", str(FPS), "-fps_mode", "cfr",
    "-preset", "medium", "-movflags", "+faststart", str(silent)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# Render Subscribe as an independent, fixed-position transparent layer. It is
# deliberately composited after the scene xfade so the CTA cannot inherit any
# scene-level movement or interpolation.
cta_overlay = OUT / "subscribe_cta.png"
run_cta_renderer(cta_overlay)
cta_start = (len(SCENES) - 1) * (SCENE_SECONDS - XFADE_SECONDS)
silent_with_cta = OUT / "silent_with_cta.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(silent), "-loop", "1", "-i", str(cta_overlay),
    "-filter_complex", f"[0:v][1:v]overlay=0:0:format=auto:enable='between(t,{cta_start:.2f},30)'[v]",
    "-map", "[v]", "-t", "30", "-c:v", "libx264", "-profile:v", "baseline",
    "-level", "4.0", "-pix_fmt", "yuv420p", "-r", str(FPS), "-fps_mode", "cfr",
    "-preset", "medium", "-movflags", "+faststart", str(silent_with_cta)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

voice = OUT / "voice.mp3"
synthesize(VOICE_TEXT, str(voice))

subprocess.run([
    "ffmpeg", "-y", "-i", str(voice), "-t", "30", "-vn", "-c:a", "aac",
    "-ar", "44100", "-ac", "2", "-b:a", "128k", "-af", "apad=pad_dur=30",
    "-movflags", "+faststart", "-f", "adts", "/tmp/voice_qa.aac"
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

video = OUT / "video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(silent_with_cta), "-i", str(voice), "-map", "0:v:0", "-map", "1:a:0", "-t", "30",
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
for path in [silent, silent_with_cta, cta_overlay]:
    path.unlink(missing_ok=True)
print(f"Verified professional 1080x1920 H.264/AAC MP4 with full Hidayat Tube branding background: {video}")
