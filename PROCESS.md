# Build history

## v6: approved look, broken loop

The typing scene got approved. But the loop blinked visibly on every restart. The first and last frames were different poses, so the animation jumped each cycle.

## v7: first loop attempt

Tried to smooth over the loop point. Still blinked. Measured it properly this time: 15% of pixels differed between the first and last frames (mean absolute difference 23.60). No amount of encoding tweaks fixes a mismatch that big. The frames just don't match.

## v8: true seamless loop (current, live)

Stopped trying to fix the endpoints. Instead, searched the clip for two frames *inside* the motion that already match each other. Typing is periodic, so the pose had to repeat somewhere.

Frame 24 and frame 216: mean difference 0.48, 12 pixels out of 875,520 differing by more than 30. Practically the same frame.

Rebuilt the video from frames 24–216 (193 frames, 8.04s at 24fps). No crossfade, no cut, no trick. The loop point is invisible because the motion genuinely continues through it.

## Dark-mode branch (v9–v30, parked)

Built a full dark variant in parallel: background keyed to near-black, figure brightness-graded so it reads on dark. Twenty-plus iterations: edge halos, the laptop lid dissolving into the background, muddy shadows, a white patch that kept surviving keying. Each version fixed exactly one thing.

It worked. I parked it anyway and shipped light-only for now. The code path is still in the page, dormant, ready to switch back on.
