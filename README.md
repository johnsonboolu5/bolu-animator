# bolu-animator

An animated version of me, living on my portfolio.

**Live:** https://bolu.info/animator

## What it is

You land on the page and a character version of me is standing there waving while a counter runs 0 to 100. Then it settles into me at a desk, typing, looping forever with no visible restart. One line underneath: *"I'm an engineer and an author. I love making 3D environments and reading."*

Purple cap, black hoodie, red cargo shorts, yellow sneakers, no socks. The no-socks detail survived every revision.

## How it's built

**Modeling.** Likeness sculpt first (head and face carry the whole thing), then body, hands, and wardrobe. Clean topology on hard-surface pieces, enough resolution in the hoodie to fold. Retopo to quads, UVs, textures. ZBrush for sculpting, Substance Painter for textures.

**Rigging.** Biped rig, IK arms for the desk work, FK for the wave, simple facial rig (eyes, brows, jaw). Hand-painted skin weights around the shoulders and elbows where the typing lives. Done on Autodesk Maya.

**Animation.** Two shots: the standing wave intro (~2s with the counter), then the seated typing cycle. Block the keys, spline, polish until the cycle runs clean. Ships as video on the page.

**Cleanup is a frame-level pass.** Edge cleanup, background keyed out to pure white, halo removal, shadow softening. Dozens of throwaway passes, each one fixing a single visible defect.

**The page is WordPress** (Hostinger, Elementor, Osty theme). All the behavior (preloader sequencing, the 0 to 100 counter, the cut into the sitting shot, responsive sizing) lives in one Code Snippets entry, JS and CSS. One header, nothing fighting anything else.

## The loop (the interesting part)

Every looping shot has the same problem: the last frame doesn't match the first, so you get a pop on each cycle. Crossfading hides it but goes mushy. I wanted a clean cycle. No tricks, no cuts.

Typing is a cycle. Hands rise and fall, and somewhere in there the pose repeats. So instead of forcing the endpoints together, I went looking for two frames inside the motion that already matched.

The process:

1. Pulled all 216 frames (9 seconds at 24fps)
2. Compared every frame against every other by mean pixel difference
3. Found it: **frame 24 and frame 216 are all but identical**. Mean difference 0.48 out of 255. Only 12 pixels out of 875,520 differ by more than 30.

   For reference, the original first and last frames were way off: mean difference 23.60, with 131,064 pixels differing. That was the pop.
4. Cut the shot to frames 24 through 216: 193 frames, 8.04 seconds. The end of the cycle is the start of the cycle. There's no seam because there's nothing to seam.

`scripts/find_loop_point.py` runs the search. `scripts/build_seamless_loop.py` makes the cut.

## Repo layout

- `assets/` - the final loop and poster frame
- `scripts/` - the frame comparison and loop cut
- `web/` - the page JavaScript and CSS
- `PROCESS.md` - build history: what broke, what fixed it
