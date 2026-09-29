#!/usr/bin/env python3
"""
build_seamless_loop.py: cut a shot down to a clean loop.

Takes the matching frame pair found by find_loop_point.py and cuts just
that range. The output's last frame flows into its first frame because
they're (nearly) the same pose. The loop point is invisible with no
crossfade and no blending.

Usage:
    python build_seamless_loop.py input.mp4 24 216 -o typing-seamless.mp4

    (frame numbers are 1-based, matching find_loop_point.py output)

Requires: ffmpeg.
"""
import argparse
import subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", help="input clip")
    ap.add_argument("start", type=int, help="first frame of loop (1-based)")
    ap.add_argument("end", type=int, help="last frame of loop (1-based)")
    ap.add_argument("-o", "--output", required=True, help="output mp4")
    ap.add_argument("--fps", type=int, default=24, help="frame rate")
    args = ap.parse_args()

    if args.end <= args.start:
        raise SystemExit("end must be after start")

    start_s = (args.start - 1) / args.fps
    frames = args.end - args.start + 1
    duration = frames / args.fps

    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{start_s:.6f}",
        "-i", args.video,
        "-t", f"{duration:.6f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", "-preset", "slow",
        "-movflags", "+faststart",
        args.output,
    ]
    print(f"Cutting frames {args.start}..{args.end} "
          f"({frames} frames, {duration:.2f}s) -> {args.output}", flush=True)
    subprocess.run(cmd, check=True)
    print("Done.", flush=True)


if __name__ == "__main__":
    main()
