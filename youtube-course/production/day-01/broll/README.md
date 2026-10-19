# Day 01 technical B-roll

Seven short, silent, 1920×1080/30 fps instructional inserts. These are animated graphics, **not** screenshots of executed Python. Keep the real shell, VS Code and terminal proof shots from the recording as the primary evidence. Insert these as brief annotations at the placements in `manifest.json`; do not concatenate them into an invented eight-minute sequence. No narration/music is baked in.

## Rebuild

From this directory on Windows with Node 22+:

```powershell
npm.cmd ci
node render.mjs
# To re-render one modified scene without replacing the other manifest entries:
node render.mjs 05-syntax-repair
```

`render.mjs` uses project-local `ffmpeg-static` and `ffprobe-static` and HyperFrames' downloaded Chrome Headless Shell. If that browser cache is absent, run `./node_modules/.bin/hyperframes.cmd browser ensure` first. The seven `*.html` files are generated from `scenes.mjs` and `style.css`; `renders/*.mp4` and `manifest.json` are the verified deliveries. The HTML source is kept for inspection/editing. FFmpeg's local binary is v6.1.1 on the authoring machine. The browser path in `render.mjs` points to the pinned headless-shell version installed here; update it if `browser ensure` obtains another version.

## Provenance

- CLI: [`hyperframes` package in HeyGen's official repository](https://github.com/heygen-com/hyperframes/blob/main/packages/cli/README.md), npm [`hyperframes`](https://www.npmjs.com/package/hyperframes), pinned `0.8.141`. Installed project-local; `npm` metadata identified `git+https://github.com/heygen-com/hyperframes.git`. No similarly named package used.
- [Current official CLI reference](https://hyperframes.heygen.com/packages/cli): `render -c <composition.html> -o <file.mp4> --fps 30`, `lint`, and `browser ensure`.
- [Composition model](https://hyperframes.app/docs/2-concepts/1-compositions) and [paused, registered GSAP timeline](https://hyperframes.app/docs/3-guides/3-gsap-animation). Animation advances by deterministic seeks, not wall-clock CSS timing. Local GSAP is pinned in `package-lock.json`.
- Python statements and lesson sequencing: `../../../day-01-spoken-script.md` (English). In particular, a bare expression in a script executes but does not print; a missing closing parenthesis in a file produces a syntax error; `exit()` returns from Python shell to terminal.

## Visual treatment

Dark charcoal and deep blue, yellow actions, blue shell prompts and mint successful output. Eased camera drift and highlight orbs; blur is limited to entrances/exits, so held code stays sharp. The before/after syntax repair switches state at 1.78s with a short three-step fade rather than blending incorrect and correct punctuation together. Every output starts/ends black for flexible edits. The exercise card intentionally omits the solution.

## ChatGPT imagery: blocked, prompts ready

No ChatGPT image generation tool or connected browser was available in this agent session. **No AI images were generated.** If the creator has an image generation session, request these *non-code* context plates as separate 16:9 images. Do not ask a model to synthesize readable Python code or IDE screenshots:

1. **Automation:** “Create a premium editorial 16:9 image plate, 1920×1080, showing a small batch of paper invoices becoming an orderly workflow through abstract arrows and folders; charcoal background, deep blue light, restrained warm yellow accents, realistic paper texture, no people, no writing, no logos, no computer screen, no code; leave central negative space for an editor overlay.”
2. **Data:** “Create a premium editorial 16:9 image plate, 1920×1080, showing a physical arrangement of colored data tokens grouped into a clear trend on a dark charcoal desk; deep blue shadows, yellow focal accent, cinematic but truthful, no numbers, no labels, no logos, no computer screen, no code; space for a graphic overlay.”
3. **Web application:** “Create a premium editorial 16:9 image plate, 1920×1080, showing a network of abstract browser-window shapes connected by subtle blue lines, a single yellow path tracing request to response; dark charcoal and navy palette, no fake UI text, no logos, no code, no screens with readable content; balanced framing with safe text area.”
4. **AI tools (optional):** “Create a premium editorial 16:9 image plate, 1920×1080, showing an abstract collection of interconnected light nodes organized by a human hand pointing at a goal; dark navy/charcoal, restrained yellow accents, no humanoid robot, no text, no logos, no pseudo-code.”

Check generated files for visual accuracy, cropping and reuse rights before putting them in the edit. They are illustrative context, never proof of executable behavior.
