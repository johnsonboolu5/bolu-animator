# Build history

## v6: approved look, broken loop

The typing shot got approved. But the loop popped on every cycle. First and last frames were different poses, so the motion jumped at the restart.

## v7: first loop attempt

Tried to smooth over the loop point. Still popped. Measured it properly: 15% of pixels differed between the first and last frames (mean difference 23.60). No encode setting fixes a mismatch that big. The frames just don't match.

## v8: clean cycle (current, live)

Stopped trying to fix the endpoints. Went looking for two frames inside the motion that already matched. Typing is a cycle, so the pose had to repeat somewhere.

Frame 24 and frame 216: mean difference 0.48, 12 pixels out of 875,520 differing by more than 30. Same frame, for all practical purposes.

Cut the shot to frames 24-216 (193 frames, 8.04s at 24fps). No crossfade, no cut, no trick. The loop point is invisible because the motion genuinely continues through it.

## Dark version (v9-v30, parked)

Built a full dark variant in parallel: background keyed to near-black, figure re-graded so it reads on dark. Twenty-plus passes: edge halos, the laptop lid dissolving into the background, muddy shadows, one white patch that kept surviving the key. Each pass fixed exactly one thing.

It worked. I parked it and shipped light-only for now. The code path is still in the page, dormant, ready to switch back on.
