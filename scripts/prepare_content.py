"""Build a cinematic, branded Urdu Islamic YouTube Short for private review."""
from pathlib import Path
from datetime import datetime, timezone
import os
import subprocess

from PIL import Image, ImageDraw
from scripts.generate_voice import synthesize

OUT = Path("output")
OUT.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 30
SCENE_SECONDS = 7.5
XFADE_SECONDS = 0.55
DURATION = 30
TOPIC = "نماز کیوں ضروری ہے؟ | نماز زندگی کا اصل سکون"
BRANDING_DIR = Path("assets/branding")

# Supplied Hidayat Tube artwork is used as cinematic B-roll. Each still receives
# a very slow Ken-Burns movement so the Short never feels like a static card.
BROLL = [
    BRANDING_DIR / "picture for video.png",
    BRANDING_DIR / "picture for video2.png",
    BRANDING_DIR / "video brand post sample.png",
    BRANDING_DIR / "banner2.png",
]
FALLBACK_BG = BRANDING_DIR / "bg.png"

SCENES = [
    "کیا آپ زندگی کی الجھنوں سے پریشان ہیں؟\nنماز… سکونِ قلب کا راستہ ہے۔",
    "نماز دین کا مضبوط ستون ہے۔\nنماز اللہ سے قربت کا ذریعہ ہے۔\nنماز گناہوں سے بچنے میں مدد دیتی ہے۔",
    "نماز بے حیائی سے روکتی ہے۔\nنماز سکونِ قلب کا ذریعہ ہے۔\nنماز جنت کی کنجی ہے۔",
    "آئیے! نماز کو اپنی زندگی کا حصہ بنائیں۔\nاور اصل کامیابی حاصل کریں۔\n\nLike • Share • Subscribe",
]
VOICE_TEXT = (
    "کیا آپ زندگی کی الجھنوں سے پریشان ہیں؟ "
    "نماز دین کا مضبوط ستون ہے، اور اللہ سے قربت کا ذریعہ ہے۔ "
    "نماز ہمیں گناہوں اور بے حیائی سے بچانے میں مدد دیتی ہے۔ "
    "نماز سکونِ قلب کا ذریعہ ہے، اور جنت کی کنجی ہے۔ "
    "آئیے! نماز کو اپنی زندگی کا حصہ بنائیں اور اصل کامیابی حاصل کریں۔"
)
SCRIPT = (
    f"# {TOPIC}\n\n{VOICE_TEXT}\n\n"
    "نوٹ: قرآن و حدیث کے اصل حوالہ جات اشاعت سے پہلے مستند ذریعے سے انسانی طور پر verify کیے جائیں۔\n"
)
metadata = (
    f"topic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\n"
    f"duration_target_seconds: {DURATION}\nformat: YouTube Shorts 9:16\nresolution: {W}x{H}\n"
    f"frame_rate: {FPS}\nvoice: Microsoft Edge Neural Urdu ({os.getenv('TTS_VOICE', 'ur-PK-AsadNeural')})\n"
    "video_codec: H.264 Baseline\naudio_codec: AAC-LC\nsubscriber_cta: enabled\n"
    "like_cta: enabled\nshare_cta: enabled\nvisual_style: Cinematic Hidayat Tube black-and-gold Islamic B-roll\n"
    "font: Noto Nastaliq Urdu via Chromium Playwright\ntext_renderer: Chromium RTL/complex-text shaping\nstatus: REVIEW_REQUIRED\n"
)
(OUT / "script.md").write_text(SCRIPT, encoding="utf-8")
(OUT / "metadata.txt").write_text(metadata, encoding="utf-8")


def _cover_resize(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    img = img.convert("RGB")
    scale = max(size[0] / img.width, size[1] / img.height)
    resized = img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - size[0]) // 2)
    top = max(0, (resized.height - size[1]) // 2)
    return resized.crop((left, top, left + size[0], top + size[1]))


def make_background(path: Path, source: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Required Hidayat Tube branding artwork is missing: {source}")
    img = _cover_resize(Image.open(source), (W, H))
    draw = ImageDraw.Draw(img, "RGBA")
    # Keep the supplied artwork prominent; only add a subtle cinematic veil and
    # a gold frame so Urdu Nastaliq remains readable without becoming a generic card.
    draw.rectangle((0, 0, W, H), fill=(0, 0, 0, 34))
    draw.rectangle((28, 28, W - 28, H - 28), outline=(190, 155, 70, 190), width=4)
    draw.rectangle((52, 52, W - 52, H - 52), outline=(255, 255, 255, 45), width=1)
    draw.rounded_rectangle((58, 430, W - 58, 1490), radius=52,
                           fill=(5, 8, 16, 126), outline=(190, 155, 70, 205), width=3)
    draw.rounded_rectangle((98, 468, W - 98, 510), radius=18,
                           fill=(190, 155, 70, 220))
    img.save(path, format="PNG", optimize=True)


def run_renderer(title: str, body: str, footer: str, output: Path) -> None:
    subprocess.run(["python", "scripts/render_text.py", title, body, footer, str(output)], check=True)


def run_cta_renderer(output: Path) -> None:
    subprocess.run(["python", "scripts/render_text.py", "--cta", str(output)], check=True)


def make_motion_scene(background: Path, output: Path, direction: int) -> None:
    # Very slow push-in plus a tiny horizontal drift; 7.5 seconds / 30 fps.
    zoom_expr = "min(zoom+0.00075,1.12)"
    if direction % 2:
        x_expr = "iw/2-(iw/zoom/2)+sin(on/70)*18"
    else:
        x_expr = "iw/2-(iw/zoom/2)-sin(on/70)*18"
    y_expr = "ih/2-(ih/zoom/2)"
    vf = (
        "scale=1220:2170:force_original_aspect_ratio=increase,"
        "crop=1220:2170,"
        f"zoompan=z='{zoom_expr}':x='{x_expr}':y='{y_expr}':d=1:s=1080x1920:fps=30,"
        "eq=contrast=1.03:saturation=0.92:brightness=-0.02,format=yuv420p"
    )
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(background), "-vf", vf,
        "-t", str(SCENE_SECONDS), "-r", str(FPS), "-an", "-c:v", "libx264",
        "-profile:v", "baseline", "-level", "4.0", "-pix_fmt", "yuv420p", str(output)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


scene_videos = []
for i, text in enumerate(SCENES, 1):
    bg = OUT / f"scene_{i}_background.png"
    overlay = OUT / f"scene_{i}_text.png"
    scene_video = OUT / f"scene_{i}.mp4"
    source = BROLL[(i - 1) % len(BROLL)] if BROLL else FALLBACK_BG
    if not source.exists():
        source = FALLBACK_BG
    make_background(bg, source)
    run_renderer(TOPIC, text, f"HIDAYAT TUBE • منظر {i}", overlay)
    motion = OUT / f"scene_{i}_motion.mp4"
    make_motion_scene(bg, motion, i)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(motion), "-loop", "1", "-i", str(overlay),
        "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p,setsar=1",
        "-t", str(SCENE_SECONDS), "-r", str(FPS), "-c:v", "libx264", "-profile:v", "baseline",
        "-level", "4.0", "-pix_fmt", "yuv420p", "-an", str(scene_video)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    motion.unlink(missing_ok=True)
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
    "-map", f"[{current}]", "-t", str(DURATION), "-c:v", "libx264", "-profile:v", "baseline",
    "-level", "4.0", "-pix_fmt", "yuv420p", "-r", str(FPS), "-fps_mode", "cfr",
    "-preset", "medium", "-movflags", "+faststart", str(silent)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

cta_overlay = OUT / "subscribe_cta.png"
run_cta_renderer(cta_overlay)
cta_start = (len(SCENES) - 1) * (SCENE_SECONDS - XFADE_SECONDS)
silent_with_cta = OUT / "silent_with_cta.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(silent), "-loop", "1", "-i", str(cta_overlay),
    "-filter_complex", f"[0:v][1:v]overlay=0:0:format=auto:enable='between(t,{cta_start:.2f},{DURATION})'[v]",
    "-map", "[v]", "-t", str(DURATION), "-c:v", "libx264", "-profile:v", "baseline",
    "-level", "4.0", "-pix_fmt", "yuv420p", "-r", str(FPS), "-fps_mode", "cfr",
    "-preset", "medium", "-movflags", "+faststart", str(silent_with_cta)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

voice = OUT / "voice.mp3"
synthesize(VOICE_TEXT, str(voice))
video = OUT / "video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-i", str(silent_with_cta), "-i", str(voice), "-map", "0:v:0", "-map", "1:a:0", "-t", str(DURATION),
    "-c:v", "libx264", "-profile:v", "baseline", "-level", "4.0", "-pix_fmt", "yuv420p",
    "-r", str(FPS), "-fps_mode", "cfr", "-c:a", "aac", "-profile:a", "aac_low", "-ar", "44100",
    "-ac", "2", "-b:a", "128k", "-af", f"apad=pad_dur={DURATION}", "-movflags", "+faststart", str(video)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

probe = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries",
    "format=format_name,duration:stream=index,codec_type,codec_name,profile,pix_fmt,r_frame_rate,sample_rate,channels,width,height",
    "-of", "default=noprint_wrappers=1", str(video)
], check=True, capture_output=True, text=True)
print(probe.stdout)
required = ["codec_type=video", "codec_name=h264", "pix_fmt=yuv420p", "codec_type=audio", "codec_name=aac", f"width={W}", f"height={H}"]
if any(x not in probe.stdout for x in required):
    raise SystemExit("Generated MP4 failed stream/resolution checks")
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
print(f"Verified cinematic 1080x1920 H.264/AAC MP4 with Hidayat Tube branding: {video}")
