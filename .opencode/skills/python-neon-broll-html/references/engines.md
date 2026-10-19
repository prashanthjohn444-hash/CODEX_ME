# Output targets: HTML player, HyperFrames, Remotion

One scene file feeds all three: `node scripts/build.js scene.js <outDir> --target all` (or `html`, `hyperframes`, `remotion`).
Pick by what the creator edits in: **HyperFrames** (HTML + GSAP, `npx hyperframes`), **Remotion** (React), or the plain **HTML player** (quick preview, screen recording).

## HyperFrames (`<outDir>/hyperframes/index.html`)
Follows the documented composition contract (checked against hyperframes.heygen.com/reference/html-schema):
- Root `<div id="root" data-composition-id="main" data-start="0" data-duration=… data-width="1920" data-height="1080" data-fps="30">`.
- One `class="clip"` section with `id`, `data-start`, `data-duration`, `data-track-index`, as a **direct child** of the root; the whole scene lives inside it.
- One finite GSAP timeline, `{paused:true}`, registered as `window.__timelines.main` (same key as `data-composition-id`), pinned to the composition length. GSAP is loaded from jsDelivr, pinned to 3.14.2.
- No CSS transitions or animations (rendering is seek-based), no wall-clock state, no random, no infinite repeats. Every change is a timeline tween.
- `set:` text changes are pre-rendered versions of the text that are switched with `tl.set` (opacity), because text changes made in callbacks are not seek-safe.
- Layout space for code/result lines is reserved up front (only opacity animates), so nothing jumps.
- Theme colours are baked into the timeline's tweens from `assets/themes.js`, so a `paper` or `terminal` scene needs no extra work.
Use: `cd <outDir>/hyperframes && npx hyperframes lint && npx hyperframes check && npx hyperframes preview`, then `npx hyperframes render`. Or copy `index.html` into a project made with `npx hyperframes init`, or into a nested composition (wrap per the schema: `<template>`, matching ids and timeline key).
Offline/fonts: vendor `gsap.min.js` next to the file and change the script `src` if the render machine has no internet; add `@font-face` for Bebas Neue/Barlow or install them locally.

## Remotion (`<outDir>/remotion/`)
Real React components, 1920×1080 at 30 fps, driven by one pure function `stateAt(steps, t)` (no hooks, timers or CSS transitions), so every frame is deterministic.
`npm install`, `npm run studio`, `npm run render`. Edit `src/scene.json` (text, step times) or `src/SceneView.tsx` (layouts, colours). Duration = scene duration + 1.8 s.
Only the `remotion` package is needed for the component; fonts can be bundled with `@remotion/google-fonts`.

## Verification status
Checked here without a browser render: the HTML player and the HyperFrames timeline were run with a simulated browser and real GSAP (seeked to several times and back to 0), and the Remotion component was type-checked and rendered to markup at several frames. `hyperframes lint/check` and `remotion render` were not run in this environment; run them once on your machine and look at a frame.

## Porting by hand
- HyperFrames ↔ Remotion: HyperFrames publishes a `remotion-to-hyperframes` skill for ports of other Remotion work.
- A new layout must exist in all three: `assets/layouts.js` (HTML + HyperFrames markup), `assets/remotion/src/SceneView.tsx`, and the same step commands. A new theme is one entry in `assets/themes.js`.
- Built layouts: lanes, decision, loop, flow, compare.
