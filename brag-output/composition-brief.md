# HyperFrames Composition Brief: Python 30 Days

## Objective
Create a 20-second vertical reel in the brag workflow for the Python 30 Days course. Make its first Python puzzle and real Day 1 capture the centerpiece.

## Output
- Composition: `brag-output/composition/`
- Video after review/approval: `brag-output/brag.mp4`
- 1080×1920, 20 seconds, no voiceover.

## Source material
- Local source: `C:\Users\lms-work\Downloads\PYTHON_30_DAYS_LAB_WITH_MIND_MAPS_FIXED.html`
- Supporting source: `youtube-course/day-01-spoken-script.md`, `youtube-course/production/day-01/output/review-repair-actual.png`
- Real screenshot MUST be cropped to remove private paths before copied to the composition.
- Product name: Python 30 Days. On-screen grounded lines: `Day 1`, `Run Your First Python File`, `print(10 + 20)`, `30`, `Hello, Python!`, `Mind Maps`.

## Creative direction
Default brag tone; editorial first-code-win. Hook: why the expression prints in the shell but not in a saved file. The visual payoff is adding `print(...)` and getting `30`. No promise of 30 published videos or guaranteed job results. No fake course URL.

## Visual identity
Source lab: background `#2b2b2b`, text `#f4f4ef`, yellow `#f0c94d`, blue `#6aa8ff`, code `#1e1e1e`; Times New Roman display, Space Grotesk body (fall back to local sans if unavailable). Actual code crop visible in Scene 2.

## Storyboard
Follow `brag-plan.md`: 0–3 puzzle, 3–8 real code view, 8–13 print correction, 13–16 lesson path, 16–20 final invitation. Keep text fully settled for reading, top/bottom social safe zones, no private paths.

## Audio
- Bundled music `happy-beats-business-moves-vol-10-by-ende-dot-app.mp3`, restrained level and end fade; cue preset in brag skill assets, ~110 BPM, 15.82s strong cue.
- Sparse local SFX: soft UI click, warm reveal, one logo hit, timed to motion. No voice or captions.
- Subtle audio-reactive yellow highlight was considered, but the installed extraction helper cannot run here (`ModuleNotFoundError: numpy`). Keep the intentional cue-led glow rather than simulate audio reactivity or add new dependencies.

## Implementation
HyperFrames owns timeline and media playback. One paused, seek-safe timeline; local assets only; `hyperframes check` before preview; local rendering only after final preview approval. Use the current `/hyperframes-core`, `/hyperframes-animation`, `/hyperframes-creative`, `/hyperframes-keyframes`, `/hyperframes-cli` contracts.
