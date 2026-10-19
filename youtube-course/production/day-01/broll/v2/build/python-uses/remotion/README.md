# Python neon B-roll — Remotion project
Generated from a scene file by `node scripts/build.js scene.js <outDir> --target remotion`.

    npm install
    npm run studio      # live preview, scrub the timeline
    npm run render      # out/broll.mp4 (1920x1080, 30 fps)
    npm run still       # out/end.png (a frame to check the end state)

**Where to edit**
- `src/scene.json` — everything the scene shows (code lines, cells, output, `steps` times). Change a step time and the animation moves; no React changes needed. Rebuild from `scene.js` to regenerate it.
- `src/timeline.ts` — pure function `stateAt(steps, t)`: the state at any time `t` (so any frame renders the same every time, with no `useState`, `setTimeout` or CSS transitions).
- `src/SceneView.tsx` — the three layouts (`lanes`, `decision`, `loop`) as plain React components; colours are constants at the top (green input, violet memory, cyan output).
- `src/Root.tsx` — fps (30), size (1920x1080), duration = scene duration + 1.8 s hold.

**Fonts:** Bebas Neue and Barlow are used if installed. To bundle them, add `@remotion/google-fonts` and call `loadFont()` in `Broll.tsx`.
