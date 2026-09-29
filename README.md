# bolu-animator

An animated version of me, living on my portfolio.

**Live:** https://bolu.info/animator

## What it is

You land on the page. A 3D character version of me stands there waving while a counter runs 0 to 100. Then it cuts to me sitting at a desk, typing, on an infinite loop that never visibly restarts. One line underneath: *"I'm an engineer and an author. I love making 3D environments and reading."*

The whole thing is me: purple cap, black hoodie, red cargo shorts, yellow sneakers, no socks. The no-socks detail survived every revision.

## How it's built

**The animation is AI-generated video, made from my likeness.** I art-directed it the way you'd art-direct an illustrator: outfit, pose, pacing, expression. The brief for the final scene was simple: typing only, slow, eyes open, full figure. Then iterate until the motion looks right.

**The cleanup is frame-level Python.** Raw AI video comes out with rough edges, dirty backgrounds, halos around the figure. I extract every frame and run them through PIL/NumPy pipelines: edge cleanup, background keying to pure white, halo removal, shadow softening. Dozens of throwaway iterations, each one fixing a single visible defect.

The two scripts I kept are the loop tools. They're the interesting part, documented below.

**The page is WordPress** (Hostinger, Elementor, Osty theme). All the behavior (the preloader sequencing, the 0→100 counter, the transition into the sitting scene, responsive sizing on every screen) lives in one Code Snippets entry (JS + CSS). One header, nothing fighting anything else.

## The seamless loop (the interesting part)

The typing clip is a loop, and loops have a classic problem: the last frame doesn't match the first, so you get a visible blink every cycle. Crossfading hides it but looks mushy. I wanted a true seamless loop. No trick, no cut.

So instead of forcing the endpoints together, I searched the clip for two frames *inside* the motion that already match. Typing is periodic (hands rise and fall in a cycle), so somewhere in there, the pose repeats itself.

The analysis:

1. Extracted all 216 frames (9 seconds at 24fps)
2. Compared frames against each other by mean absolute pixel difference
3. Found it: **frame 24 and frame 216 are nearly identical**: mean difference 0.48 out of 255, only 12 pixels out of 875,520 differing by more than 30

   For comparison, the original first and last frames had a mean difference of 23.60, with 131,064 pixels differing. That was the blink.
4. Rebuilt the video from frames 24–216 only: 193 frames, 8.04 seconds. The end of the loop *is* the start of the loop. There's no seam because there's nothing to seam.

`scripts/find_loop_point.py` does the search. `scripts/build_seamless_loop.py` does the rebuild.

## Repo layout

- `assets/` - the final loop video and poster frame
- `scripts/` - frame analysis and loop rebuild
- `web/` - the page JavaScript and CSS that run the experience
- `PROCESS.md` - build history: what broke, what fixed it
