"""Add a local neural voice-over (Kokoro-82M, ONNX) to the promo video.

usage: python narrate.py en|pt --model kokoro-q8.onnx --voices voices.npz
Reads out/llminjection-promo-<lang>.mp4, writes out/llminjection-promo-<lang>-narrated.mp4.
Model and voices are not vendored; see README.md for where to get them.
"""

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from kokoro_onnx import Kokoro

HERE = Path(__file__).parent
GAP = 0.25  # minimum silence between lines, seconds

ap = argparse.ArgumentParser()
ap.add_argument("lang", choices=["en", "pt"])
ap.add_argument("--model", required=True)
ap.add_argument("--voices", required=True)
ap.add_argument("--video", default=None)
args = ap.parse_args()

cfg = json.loads((HERE / "narration.json").read_text())[args.lang]
video = Path(args.video or HERE / "out" / f"llminjection-promo-{args.lang}.mp4")
out_mp4 = video.with_name(video.stem + "-narrated.mp4")

dur = float(
    subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
)

tts = Kokoro(args.model, args.voices)
clips, sr, cursor = [], 24000, 0.0
for start, text in cfg["lines"]:
    audio, sr = tts.create(text, voice=cfg["voice"], lang=cfg["lang"], speed=cfg["speed"])
    at = max(start, cursor + GAP)
    clips.append((at, audio))
    cursor = at + len(audio) / sr
    flag = "  << shifted" if at > start + 0.05 else ""
    print(f"{at:6.2f}-{cursor:6.2f}s  {text[:60]}{flag}")

total = max(dur, cursor + 0.8)
track = np.zeros(int(total * sr) + 1, dtype=np.float32)
for at, audio in clips:
    i = int(at * sr)
    track[i : i + len(audio)] += audio
peak = float(np.abs(track).max()) or 1.0
track = (track / peak * 0.89).astype(np.float32)

wav = out_mp4.with_suffix(".wav")
pcm = (track * 32767).astype("<i2").tobytes()
subprocess.run(
    ["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(sr), "-ac", "1", "-i", "-", str(wav)],
    input=pcm,
    check=True,
)
pad = max(0.0, total - dur)
vf = ["-vf", f"tpad=stop_mode=clone:stop_duration={pad:.2f}"] if pad > 0 else []
venc = ["-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p"] if pad > 0 else ["-c:v", "copy"]
subprocess.run(
    ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(wav), *vf, *venc,
     "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
     "-map", "0:v:0", "-map", "1:a:0", "-movflags", "+faststart", "-shortest", str(out_mp4)],
    check=True,
)
wav.unlink()
print(out_mp4, f"{total:.1f}s")
