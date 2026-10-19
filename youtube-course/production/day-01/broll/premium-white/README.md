# Premium white-grid technical B-roll

New non-destructive Day 1 revision. Original dark graphics remain in `../renders/`.

The design uses a warm white canvas, fine pale-blue grid, architectural dividers, crisp dark code and restrained blue accents. It incorporates the registry's `dynamic-grid` background primitive (installed under `compositions/components/`), adapted for a light technical field. The graphic text is illustrative, not OBS footage. `09-shell-vs-file` now identifies the saved source as `expression_only.py` instead of incorrectly calling it `hello.py`.

`scenes.mjs` is the source of the authored beats. `render.mjs` builds each scene into `index.html`, runs `hyperframes check`, renders a silent 1920×1080/30 fps MP4 in `renders/`, and records exact frames in `manifest.json`. The corresponding standalone HTML is archived under `source/`. The `../package.json` dependency was upgraded from `hyperframes@0.8.141` to `0.8.144` and the updated CLI passed a full check.

The white grid cards are full-frame educational inserts, not simulations of VS Code, Python's installer, or a website visit. The missing extension/installer/greeting-edit OBS pickups remain unrecorded; this edit uses only existing genuine OBS takes when a screen demonstration is needed.
