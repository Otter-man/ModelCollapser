#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

"""Build MP4s from numeric PNG sequences.

Detects sequences that start at 01.png and encodes up to the last
consecutive image present (e.g., 01.png..74.png or 01.png..100.png).
"""

# ~3.03 fps (100 frames over ~33s)
FPS = 100 / 33

def last_consecutive_frame(dirpath: Path) -> int:
    """Return the last consecutive frame number starting from 1 if 01.png exists, else 0.

    Example: if 01..74.png exist and 75.png does not, returns 74.
    """
    if not (dirpath / "01.png").exists():
        return 0
    n = 1
    while (dirpath / f"{n:02d}.png").exists():
        n += 1
    return n - 1

def out_name(root: Path, dirpath: Path) -> Path:
    rel = dirpath.relative_to(root)
    stem = "__".join(rel.parts)
    return root / f"{stem}.mp4"

def build_movie(dirpath: Path, out_path: Path, frames: int) -> None:
    pattern = str(dirpath / "%02d.png")  # 01..NN
    cmd = [
        "ffmpeg",
        "-y",
        "-loglevel", "error", "-stats",
        "-framerate", f"{FPS:.6f}",
        "-start_number", "1",
        "-i", pattern,
        "-frames:v", str(frames),
        "-c:v", "libx264",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out_path),
    ]
    print(f"[ffmpeg] {dirpath} (1..{frames:02d}) -> {out_path.name} @ {FPS:.6f} fps")
    subprocess.run(cmd, check=True)

def main():
    root = Path.cwd()
    for dirpath, dirnames, filenames in os.walk(root):
        p = Path(dirpath)
        # skip hidden dirs
        if any(part.startswith(".") for part in p.relative_to(root).parts if part):
            continue
        try:
            n = last_consecutive_frame(p)
            if n >= 1:
                out_path = out_name(root, p)
                build_movie(p, out_path, n)
        except subprocess.CalledProcessError as e:
            print(f"[warn] ffmpeg failed in {p}: {e}")
        except Exception as e:
            print(f"[warn] unexpected error in {p}: {e}")

if __name__ == "__main__":
    main()
