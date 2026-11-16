from pathlib import Path
import subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont
from app.config import settings

W, H = 1080, 1920
BG = (10, 15, 30)
CYAN = (34, 211, 238)
WHITE = (245, 248, 255)
MUTED = (155, 174, 195)


def _font(size: int):
    candidates = ["C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def render_short(draft_id: str, title: str, narration: str, beats: list[str], audio_path: str | None = None) -> str:
    outdir = Path(settings.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    frames = outdir / f"{draft_id}_frames"
    frames.mkdir(exist_ok=True)
    chunks = [title] + beats[:5] + ["GAME ON 60 | FOLLOW FOR MORE"]
    for idx, chunk in enumerate(chunks):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        # Original geometric brand treatment; no third-party artwork.
        d.rounded_rectangle((55, 55, W-55, H-55), radius=42, outline=CYAN, width=5)
        d.rectangle((55, 240 + idx*9, W-55, 252 + idx*9), fill=CYAN)
        d.text((90, 110), "GAME ON 60", font=_font(48), fill=CYAN)
        d.text((90, 330), f"{idx+1:02d} / {len(chunks):02d}", font=_font(34), fill=MUTED)
        lines = textwrap.wrap(chunk, width=22)
        y = 650 if len(lines) <= 3 else 500
        for line in lines:
            box = d.textbbox((0, 0), line, font=_font(70))
            d.text(((W-(box[2]-box[0]))//2, y), line, font=_font(70), fill=WHITE)
            y += 100
        d.text((90, H-190), "GAMING • FACTS • STORIES", font=_font(30), fill=MUTED)
        img.save(frames / f"frame_{idx:02d}.png")
    video = outdir / f"{draft_id}.mp4"
    cmd = ["ffmpeg", "-y", "-framerate", "1/7", "-i", str(frames / "frame_%02d.png")]
    if audio_path:
        cmd += ["-i", audio_path, "-map", "0:v:0", "-map", "1:a:0", "-c:a", "aac", "-shortest"]
    cmd += ["-vf", "scale=1080:1920,format=yuv420p", "-r", "30", "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video)]
    subprocess.run(cmd, check=True, capture_output=True)
    return str(video)
