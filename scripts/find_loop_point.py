#!/usr/bin/env python3
"""
find_loop_point.py: find two frames inside a clip that match closely enough
to form a true seamless loop.

The problem: a looping clip blinks when its last frame doesn't match its
first. Crossfading hides the blink but looks mushy.

The insight: periodic motion (typing, breathing, idle sway) repeats poses
*inside* the clip. If you find two matching frames in the middle of the
motion, you can cut the clip to just that range. The end of the loop
genuinely continues into the start. No seam, because there's nothing to seam.

Method:
    1. Extract every frame with ffmpeg.
    2. Compare each frame against every later frame using mean absolute
       pixel difference (cheap, and good enough: we're looking for
       near-identical poses, not perceptual similarity).
    3. Report the pair with the lowest difference, plus how bad the
       naive first-vs-last pairing is for comparison.

Usage:
    python find_loop_point.py input.mp4 [--workdir ./frames]

Requires: ffmpeg, Python 3, numpy, Pillow.
"""
import argparse
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image


def extract_frames(video_path, workdir):
    os.makedirs(workdir, exist_ok=True)
    pattern = os.path.join(workdir, "f%03d.png")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", video_path, pattern],
        check=True,
    )
    files = sorted(f for f in os.listdir(workdir) if f.endswith(".png"))
    return [os.path.join(workdir, f) for f in files]


def load_small(path, max_w=480):
    """Downscale for speed: pose matching doesn't need full resolution."""
    img = Image.open(path).convert("RGB")
    if img.width > max_w:
        img = img.resize((max_w, int(img.height * max_w / img.width)))
    return np.array(img).astype(np.float32)


def mean_abs_diff(a, b):
    return float(np.abs(a - b).mean())


def count_hot_pixels(a, b, threshold=30):
    return int((np.abs(a - b).max(axis=2) > threshold).sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", help="input clip, e.g. typing-v7.mp4")
    ap.add_argument("--workdir", default="./frames",
                    help="where to dump extracted frames")
    ap.add_argument("--min-gap", type=int, default=24,
                    help="minimum frames apart for a candidate pair "
                         "(avoids matching a frame with its neighbor)")
    args = ap.parse_args()

    print(f"Extracting frames from {args.video} ...", flush=True)
    frame_files = extract_frames(args.video, args.workdir)
    n = len(frame_files)
    print(f"{n} frames extracted.", flush=True)

    print("Loading frames ...", flush=True)
    frames = [load_small(p) for p in frame_files]
    total_px = frames[0].shape[0] * frames[0].shape[1]

    # Baseline: how bad is the naive loop point?
    naive = mean_abs_diff(frames[0], frames[-1])
    naive_hot = count_hot_pixels(frames[0], frames[-1])
    print(f"\nNaive first-vs-last: mean diff {naive:.2f}, "
          f"{naive_hot:,} of {total_px:,} px differ by >30 "
          f"({100.0 * naive_hot / total_px:.1f}%)")

    print("Searching for the best matching pair ...", flush=True)
    best = None
    for i in range(n):
        for j in range(i + args.min_gap, n):
            d = mean_abs_diff(frames[i], frames[j])
            if best is None or d < best[2]:
                best = (i, j, d)

    i, j, d = best
    hot = count_hot_pixels(frames[i], frames[j])
    print(f"\nBest pair: frame {i + 1} and frame {j + 1} "
          f"(1-based, {n} frames total)")
    print(f"  mean diff: {d:.2f} / 255")
    print(f"  pixels differing by >30: {hot:,} of {total_px:,}")
    print(f"\nSeamless loop = frames {i + 1}..{j + 1} "
          f"({j - i + 1} frames)")


if __name__ == "__main__":
    main()
