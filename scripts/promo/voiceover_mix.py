"""Place a single-take voice-over on the video tour, line by line.

usage: python voiceover_mix.py VIDEO SPEECH TIMELINE.json OUT.mp4 [HOLDS]
HOLDS (optional) freezes frames to make room for longer lines, e.g. "14.85:2.6,23.69:1.3"
(hold the frame at 14.85 s for 2.6 s, and at 23.69 s for 1.3 s); later beats move with it.
The take is one audio file with the narration lines separated by long pauses
([long pause] in ElevenLabs v4). The longest silences split it into lines; each
line starts at its beat in the timeline (or just after the previous line ends).
Needs ffmpeg and numpy.
"""

import json
import subprocess
import sys

import numpy as np

SR = 48000
BEATS = ["intro", "stats", "graph", "g_select", "g_focus", "g_open", "ch2", "c_heat", "c_drill", "c_gaps", "c_actors", "outro"]
LEAD = {"intro": 0.35, "stats": 0.15, "graph": 0.5, "ch2": 0.25, "outro": 0.2}  # seconds after the beat
GAP = 0.2


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def split(audio, n_lines):
    hop = SR // 100
    frames = len(audio) // hop
    rms = np.sqrt(np.mean(audio[: frames * hop].reshape(frames, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms / rms.max())
    quiet = db < -42
    runs, i = [], 0
    while i < frames:
        if quiet[i]:
            j = i
            while j < frames and quiet[j]:
                j += 1
            if i > 0 and j < frames:
                runs.append((j - i, i, j))
            i = j
        else:
            i += 1
    cuts = sorted(sorted(runs, reverse=True)[: n_lines - 1], key=lambda r: r[1])
    loud = np.where(~quiet)[0]
    start, segs = loud[0], []
    for _, a, b in cuts:
        segs.append((start * hop, a * hop))
        start = b
    segs.append((start * hop, (loud[-1] + 1) * hop))
    pad = int(0.04 * SR)
    return [audio[max(0, a - pad): b + pad] for a, b in segs], [r[0] / 100 for r in cuts]


def hold_frames(video, holds, out):
    """Freeze the frame at each time for the given seconds (holds = [(t, secs), ...]); returns the new file."""
    parts, prev, chains = [], 0.0, []
    for k, (t, d) in enumerate(sorted(holds)):
        chains.append(f"[0:v]trim={prev}:{t},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={d}[v{k}]")
        parts.append(f"[v{k}]")
        prev = t
    chains.append(f"[0:v]trim=start={prev},setpts=PTS-STARTPTS[v{len(holds)}]")
    parts.append(f"[v{len(holds)}]")
    graph = ";".join(chains) + ";" + "".join(parts) + f"concat=n={len(parts)}:v=1:a=0[v]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-filter_complex", graph, "-map", "[v]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", out], check=True)
    return out


video, speech, timeline, out = sys.argv[1:5]
holds = [tuple(map(float, h.split(":"))) for h in sys.argv[5].split(",")] if len(sys.argv) > 5 and sys.argv[5] else []
marks = json.load(open(timeline))["marks"]
if holds:
    video = hold_frames(video, holds, out + ".held.mp4")
    marks = {k: v + sum(d for t, d in holds if v >= t) for k, v in marks.items()}
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                           capture_output=True, text=True, check=True).stdout)
lines, gaps = split(decode(speech), len(BEATS))
print("split gaps (s):", [round(g, 2) for g in gaps])
placed, cursor = [], 0.0
for beat, clip in zip(BEATS, lines, strict=True):
    want = marks[beat] + LEAD.get(beat, 0.25)
    at = max(want, cursor + GAP)
    cursor = at + len(clip) / SR
    placed.append((at, clip))
    print(f"{beat:9s} {at:6.2f}-{cursor:6.2f}s ({len(clip) / SR:4.1f}s){'  << shifted %.2fs' % (at - want) if at > want + 0.05 else ''}")
total = max(dur, cursor + 0.9)
track = np.zeros(int(total * SR) + 1, dtype=np.float32)
for at, clip in placed:
    i = int(at * SR)
    track[i: i + len(clip)] += clip
track = track / max(1e-6, float(np.abs(track).max())) * 0.89
wav = out + ".wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", wav],
               input=track.astype("<f4").tobytes(), check=True)
pad = total - dur
venc = (["-vf", f"tpad=stop_mode=clone:stop_duration={pad:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p"]
        if pad > 0.05 else ["-c:v", "copy"])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-i", wav, *venc, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-map", "0:v:0", "-map", "1:a:0", "-movflags", "+faststart",
                "-shortest", out], check=True)
print(out, f"{total:.1f}s")
