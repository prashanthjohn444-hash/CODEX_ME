# Day 1 B-roll — batch report (`broll\v2`)

**Topic:** Run Your First Python File · **Skill:** python-neon-broll-html · **Batch built:** 2026-10-17
**Spec:** 1920×1080, 30 fps, H.264 MP4 (Rec.709 / SDR 8-bit yuv420p) · clips ≤ 4.5 s incl. 0.4 s hold · motion starts ≤ 0.3 s
**Interpreter used for every printed line:** Python 3.13.15 (`python --version` → `Python 3.13.15`), win32 MSC v.1944

---

## 1. Per-scene status

| # | Scene | Scene file | Section | Duration (scene + hold) | Layout · theme | Python logo | `hyperframes lint` | `hyperframes check` | Render |
|---|-------|-----------|---------|--------------------------|----------------|-------------|--------------------|---------------------|--------|
| 1 | shell-vs-file | `scenes\shell-vs-file.js` | 01 + 09 | 4.0 + 0.4 = **4.4 s** (132 f) | compare · paper | yes (badge) | 0 err / 7 warn | 0 err / 7 warn · WCAG AA 48/48 · 0 layout errors | `renders\shell-vs-file.mp4` 678 KB |
| 2 | setup-path | `scenes\setup-path.js` | 02 | 4.0 + 0.4 = **4.4 s** (132 f) | flow · neon | yes (badge) | 0 err / 7 warn | 0 err / 7 warn · WCAG AA 71/71 · 0 layout errors | `renders\setup-path.mp4` 702 KB |
| 3 | python-uses | `scenes\python-uses.js` | 03 | 4.0 + 0.4 = **4.4 s** (132 f) | flow · paper | yes (badge) | 0 err / 7 warn | 0 err / 7 warn · WCAG AA 71/71 · 0 layout errors | `renders\python-uses.mp4` 736 KB |
| 4 | interpreter-flow | `scenes\interpreter-flow.js` | 04 | 4.0 + 0.4 = **4.4 s** (132 f) | flow · neon | yes (badge) | 0 err / 7 warn | 0 err / 7 warn · WCAG AA 71/71 · 0 layout errors | `renders\interpreter-flow.mp4` 755 KB |
| 5 | prompt-map | `scenes\prompt-map.js` | 05 | 4.0 + 0.4 = **4.4 s** (132 f) | compare · paper | yes (badge) | 0 err / 7 warn | 0 err / 7 warn · WCAG AA 55/55 · 0 layout errors | `renders\prompt-map.mp4` 792 KB |
| 6 | syntax-repair | `scenes\syntax-repair.js` | 07 | 4.0 + 0.4 = **4.4 s** (132 f) | decision · neon | yes (badge) | 0 err / 7 warn | 0 err / 7 warn · WCAG AA 58/58 · 0 layout errors | `renders\syntax-repair.mp4` 894 KB |
| 7 | file-run-cycle | `scenes\file-run-cycle.js` | 08 | 4.0 + 0.4 = **4.4 s** (132 f) | flow · neon | yes (badge) | 0 err / 7 warn | 0 err / 7 warn · WCAG AA 72/72 · 0 layout errors | `renders\file-run-cycle.mp4` 696 KB |
| 8 | type-map | `scenes\type-map.js` | 10 | 4.0 + 0.4 = **4.4 s** (132 f) | compare · paper | yes (badge) | 0 err / 7 warn | 0 err / 7 warn · WCAG AA 48/48 · 0 layout errors | `renders\type-map.mp4` 697 KB |
| 9 | challenge-card | `scenes\challenge-card.js` | 11 | 3.6 + 0.4 = **4.0 s** (120 f) | flow · paper (still-card, no logo emphasis) | none (per brief) | 0 err / 7 warn | 0 err / 7 warn · WCAG AA 74/74 · 0 layout errors | `renders\challenge-card.mp4` 712 KB |

**Warnings are identical on all nine scenes** and come from the skill's shared engine, not from scene content:
* `6 × css_transition_used` — the template's CSS `transition:` declarations (`.fade`, `.panel`, `.ln`, `.cell`, `.cell .b`, `.node`). The generated HyperFrames document overrides them with `*,*::before{transition:none!important;animation:none!important}`, and every visual change is a GSAP tween, so rendering stays seek-safe. The lint flags the declarations themselves.
* `1 × nested_structure_needs_subcomposition` — the documented builder markup places the whole scene in a single `<section class="clip">` inside `#root` (exactly the contract in `references/engines.md`). Lint would prefer the clip body in a sub-composition mounted with `data-composition-src`.
* No content warnings: no unknown step ids, no over-length lines, no over-long titles, no unresolved-logo warnings (all nine built warning-free from `scripts/build.js`; the only `!` output the builder can print is absent).

### Built output tree

```
broll\v2\
  scenes\*.js                      9 scene files
  build\<scene>\
      <scene>-broll.html           HTML player (scrub / speed / hide-controls)
      hyperframes\index.html       HyperFrames composition (paused GSAP timeline, registered as window.__timelines.main)
      remotion\                    Remotion project (React, src\scene.json + src\SceneView.tsx)
  renders\*.mp4                    9 finished clips
  report.md
```
117 files / 6.87 MB total. Nothing outside `youtube-course\production\day-01\broll\v2\` was written (tool caches for fonts/Chrome/Granite are created by the HyperFrames CLI under `%USERPROFILE%\.cache\hyperframes` — see §6).

---

## 2. Timeline per scene (clip start = 0.00 s; motion starts ≤ 0.30 s everywhere)

| Scene | 0.12 | input/code | operation | result | hold |
|---|---|---|---|---|---|
| **shell-vs-file** | heading | 0.30 `10 + 20`; 0.45 `print(10 + 20)` | 0.90 SHELL panel → 1.05 `>>> 10 + 20` / `30`, 1.40 shell lit; 1.95 FILE panel → 2.10 `10 + 20` / `nothing printed`, 2.40 file lit | 2.90 clear highlight; 2.95 + 3.35 WHY lines | last motion **3.35** → 4.40 |
| **setup-path** | heading | 0.30 destination lines (0.50 second line) | 0.90 node row; lits 1.15 SETUP · 1.65 SHELL · 2.15 FILE · 2.65 RUN | 3.05 clear; 3.10 `Hello, Python!`; 3.50 `30` | **3.50** → 4.40 |
| **python-uses** | heading | 0.30 / 0.50 same-start lines | 0.90 nodes; lits 1.15 PYTHON · 1.65 AUTOMATION · 2.15 DATA · 2.65 WEB + AI | 3.05 clear; 3.10 `Hello, Python!`; 3.50 `30` | **3.50** → 4.40 |
| **interpreter-flow** | heading | 0.30 / 0.50 hello.py lines | 0.90 nodes; lits 1.15 FILE · 1.65 COMMAND · 2.15 INTERPRETER · 2.65 OUTPUT | 3.05 clear; 3.10 `Hello, Python!`; 3.50 `30` | **3.50** → 4.40 |
| **prompt-map** | heading | 0.30 prompt key (2 lines) | 0.90 SHELL panel → 1.05 three shell lines, 1.40 lit; 1.95 TERMINAL panel → 2.10 three terminal lines, 2.40 lit | 2.90 clear; 2.95 `still in the shell → exit()`; 3.35 `then type → python hello.py` | **3.35** → 4.40 |
| **syntax-repair** | heading | 0.30 broken line; 0.45 second line | 0.85 condition `missing`; 1.15 TRUE+FALSE branch panels; 1.45 FALSE (broken) lit; 2.35 clear → 2.40 condition becomes `added`; 2.70 TRUE lit; 2.75 FALSE dimmed | 1.75 `SyntaxError: '(' was never closed`; 3.10 `repaired → Hello, Python!` | **3.10** → 4.40 |
| **file-run-cycle** | heading | 0.30 / 0.50 file lines | 0.90 nodes; lits 1.15 EDIT · 1.65 SAVE · 2.15 RUN | 2.55 TERMINAL panel; 2.65 `Hello, Python!`; 3.10 `30`; 3.50 CHANGE lit (loop returns to the edit step) | **3.50** → 4.40 |
| **type-map** | heading | 0.30 `print(30)` / 0.45 `print("30")` | 0.90 `30 · NUMBER` panel → 1.05 `type(30)` / `<class 'int'>`, 1.40 lit; 1.95 `'30' · TEXT` panel → 2.10 `type('30')` / `<class 'str'>`, 2.40 lit | 2.90 clear; 2.95 `print(30) → int`; 3.35 `print("30") → str` | **3.35** → 4.40 |
| **challenge-card** | heading | 0.30 / 0.45 / 0.60 the three challenge lines | 0.80 node row; lits 1.00 WRITE · 1.50 SAVE · 2.00 RUN · 2.50 CHANGE | 2.90 clear; 2.95 `Hello, Python!`; 3.20 `30`; 3.40 `<class 'int'>` | **3.40** → 4.00 |

Step semantics are the skill's: *state at time t = every step with time ≤ t, applied in order*, so scrubbing, looping and frame rendering agree.

---

## 3. Match-cut consistency

* Identical furniture in every scene: H1 at the same y (5.2cqw), subtitle inline to its right, logo badge right-aligned (4.4cqw) — present on scenes 1–8, deliberately absent on the still-card (9) per the brief ("sans logo emphasis").
* **compare** scenes (1, 5, 8) are identical in geometry: 2-line INPUT panel, two side-by-side panels with 2–3 lines each, 2-line result panel — same columns, paddings and gaps.
* **flow** scenes (2, 3, 4, 7, 9) all use **four nodes** with the same node row and the same 2-line input / 2- or 3-line output stack, so the node row does not shift on a cut. Values are ≤ 15 characters so no node text wraps or overflows (checked by `hyperframes check` layout inspection).
* Role colours are constant: green = the line/value that ends "clean" (INPUT, PYTHON SHELL, SHELL panel, TRUE branch), cyan = the quiet/terminal/result side, violet = process/condition. Logos keep brand colour (Python `#3776AB`), never re-tinted.
* Only `syntax-repair` uses `decision`, only scenes 1/5/8 use `compare`; the card (9) is intentionally a different, calmer card beat.

---

## 4. Python verification — every printed line, with a real run

All lines on screen are the literal output of Python 3.13.15. Commands and raw results (scratch dir `%TEMP%\opencode\day01-verify`, outside the deliverable):

| On screen | Verified command | Actual result |
|---|---|---|
| `30` | `python -c "print(10 + 20)"` | `30` |
| `Hello, Python!` | `python -c "print('Hello, Python!')"` | `Hello, Python!` |
| `<class 'int'>` | `python -c "print(type(30))"` | `<class 'int'>` |
| `<class 'str'>` | `python -c "print(type('30'))"` | `<class 'str'>` |
| (narration only: float / bool) | `python -c "print(type(3.5))"` / `print(type(True))` | `<class 'float'>` / `<class 'bool'>` |
| `nothing printed` (file with only `10 + 20`) | file `b_expr_only.py` = `10 + 20`; `python b_expr_only.py` | **no output at all**, exit code 0 |
| `python -c "10 + 20"` (same thing, script mode) | `python -c "10 + 20"` | no output |
| `>>> 10 + 20` → `30` (shell echo) | `python -i` with stdin `10 + 20\n` (subprocess capture) | stdout `'30\n'` |
| `>>> exit()` (leaves the shell) | `python -i` with stdin `exit()\n` | stdout `''`, prompt returns, exit 0 |
| `Hello, Python!` + `30` (hello.py) | `g_hello.py` = `print("Hello, Python!")`, `print(10 + 20)`; `python g_hello.py` | `Hello, Python!` then `30` |
| `SyntaxError: '(' was never closed` | file `e_broken.py` = `print("Hello, Python!"`; `python e_broken.py` | stderr last line exactly `SyntaxError: '(' was never closed` (rc 1) — also reproduced with `compile('print("Hello, Python!"', '<string>', 'exec')` |
| `repaired → Hello, Python!` | `f_fixed.py` = `print("Hello, Python!")`; `python f_fixed.py` | `Hello, Python!` |
| card: `Hello, Python!` / `30` / `<class 'int'>` | `i_challenge.py` = `print("Hello, Python!")`, `print(10 + 20)`, `print(type(30))`; `python i_challenge.py` | `Hello, Python!` / `30` / `<class 'int'>` (in that order) |
| `Python 3.13.15` (report only; section 04 uses the real terminal capture) | `python --version` | `Python 3.13.15` |

Other rules that were checked rather than assumed:
* Escape rule: the only `<` characters on screen are the two `type()` results, written as `&lt;class 'int'&gt;` / `&lt;class 'str'&gt;` in the scene files; the rendered frames show correct `<class 'int'>` text (verified in the rendered still of `type-map`).
* No other angle brackets appear anywhere in the nine scenes.
* `PS C:\python-30-days>` is a *terminal prompt* label, not claimed Python output; `python hello.py`, `python greeting.py`, `python --version`, `Ctrl+S`, `python.org`, `greeting.py`, `hello.py` are commands/filenames, not results — no result text is invented.

---

## 5. Verification of the built artifacts

**HyperFrames (primary render path).** engines.md documents `npx hyperframes lint && npx hyperframes check` … then `npx hyperframes render` for this target, so the clips were rendered with exactly those subcommands:

```
cd build\<scene>\hyperframes
npx hyperframes lint          # 0 errors, 7 warnings (see §1)
npx hyperframes check         # Lint + Runtime + Layout + Motion + Contrast, 0 errors
npx hyperframes render -o ..\..\..\renders\<scene>.mp4
```
(`npx.cmd` was used because the PowerShell `npx.ps1` shim is blocked by execution policy; it resolves to the project-local **hyperframes 0.8.144** in `broll\node_modules`. The globally installed CLI 0.8.168 at `%APPDATA%\npm\hyperframes.cmd` was confirmed present but not needed for the render. `ffmpeg`/`ffprobe` are not on PATH, so `HYPERFRAMES_FFMPEG_PATH` / `HYPERFRAMES_FFPROBE_PATH` were pointed at the existing `node_modules\ffmpeg-static\ffmpeg.exe` and `node_modules\ffprobe-static\...\ffprobe.exe`.)

* `check` results: **0 errors** on all nine; Runtime 0 errors; Layout 0 errors (an earlier build failed layout inspection — `<strong>` inside the `.res` line box clipped 15 px — which is why the result lines are now plain text); Motion 0 errors; Contrast `pass WCAG AA` for 48–74 text checks per scene.
* MP4 probe (`ffprobe`): every file `codec_name=h264`, `1920x1080`, `r_frame_rate=30/1`, `pix_fmt=yuv420p`; 132 frames / 4.400000 s for scenes 1–8 and 120 frames / 4.000000 s for the card — i.e. all clips ≤ 4.5 s.
* Frame inspection of every render (frames extracted to `%TEMP%`): **frame 0 is 90–92 % a single background colour with only 21–43 unique colours** — heading, panels and text are all still hidden (scrub-to-zero leaves nothing behind); the last frame shows 41–51 % background and ~30–42 k unique colours, i.e. the complete final state.
* Visual check of rendered end frames: heading/subtitle/logo placement, panel roles, node row and result lines are correct and nothing is clipped (`shell-vs-file`, `setup-path`, `syntax-repair`, `type-map`, `challenge-card` inspected as images).

**HTML player (all nine).** Each `build\<scene>\<scene>-broll.html` was loaded in headless Chrome (puppeteer-core + the Chrome headless shell already in the HyperFrames cache) and exercised:

* 0 page errors / 0 console errors in all nine;
* scrub to `0` → 0 of 8–15 animated elements visible, and back to `0` after the end state → 0 visible again;
* scrub to the end → all elements visible, `#o1` has real height, `set:` values resolved (e.g. syntax-repair condition `missing` → `added` → back to `missing`), and the final highlight state is `bt` (syntax-repair, fixed branch) and `n3` (file-run-cycle, CHANGE node).

**Remotion (all nine).** `build\<scene>\remotion\` is a complete project (package.json, tsconfig, `src\index.ts`, `Root.tsx`, `Broll.tsx`, `SceneView.tsx`, `timeline.ts`, `scene.json`). Verified on a copy of `type-map\remotion` in the temp dir so the deliverable stays clean: `npm install` (254 packages) + `npx tsc --noEmit` → **exit 0, no diagnostics**; `npx remotion still src/index.ts Broll out/end.png --frame=120` → **exit 0**, 188 KB PNG. That still (t = 4.0 s of the 4.0 + 1.8 s Remotion timeline) shows the same content as the HyperFrames clip: correct heading, badge, panels, node/result text and the correctly escaped `<class 'int'>` / `<class 'str'>` lines. Note the font difference: the Remotion still renders the heading in a system sans because Bebas Neue / Barlow are not installed on this machine — the HTML and HyperFrames targets embed the font faces, the Remotion project needs `@remotion/google-fonts` (or local fonts) before its type matches.

---

## 6. What was NOT verified / known limits

1. **`hyperframes preview` (the interactive studio) was not opened** — this environment is non-TTY, and no desktop browser is connected to the session, so the player/studio UI was not clicked by hand. Motion was verified instead through `check` (layout/motion gates) and through frame extraction from the renders plus scripted scrubbing of the HTML player.
2. **The Remotion target was checked, not rendered as a batch.** `npm install` + `tsc --noEmit` + one `remotion still` (frame 120 of `type-map`) all pass on a temp copy, but no Remotion MP4 was produced for the other eight scenes, and only `type-map` was opened as an image. The delivered MP4s come from the HyperFrames target, which is what engines.md documents as its render path.
3. **Windows path**: `prompt-map` shows `PS C:\python-30-days>`, matching the script's Windows recording machine. On another OS the prompt differs — that label is a location hint, not a Python result.
4. **Cells/boxes/panels are teaching metaphors.** `shell-vs-file`, `prompt-map` and `type-map` show a shell session and a file side by side; a real terminal transcript is longer, and section 04's `python --version` check is explicitly a *real capture* in the edit (production brief), with `interpreter-flow` only explaining what runs the file — the graphic must not be presented as an IDE/terminal capture.
5. **Two brief-level deviations, both deliberate and flagged:**
   * `challenge-card` carries no logo badge ("sans logo emphasis") and is 4.0 s total, so it cuts against nothing in the flow row — a card, not a flow panel.
   * `prompt-map`'s section-09 cousin is `shell-vs-file`, reused as the brief's edit map requests (scene 1 serves sections 01 and 09).
6. **Tool caches outside the deliverable:** HyperFrames writes font/Chrome caches under `%USERPROFILE%\.cache\hyperframes`, frame caches under `%TEMP%`, and the ffmpeg/ffprobe binaries are read from the pre-existing `broll\node_modules`. No other production folder was modified.
7. The Python results above were verified on **CPython 3.13.15 / win32** only. The `SyntaxError` wording (`SyntaxError: '(' was never closed`) is the 3.12+ message; older interpreters word it differently, so if the video's real capture is recorded on an older Python the graphic's error line should be re-checked against that machine.

## 7. Commands used

```powershell
# build (all three targets per scene)
node .opencode\skills\python-neon-broll-html\scripts\batch.js `
     youtube-course\production\day-01\broll\v2\scenes `
     youtube-course\production\day-01\broll\v2\build --target all

# logos (offline, from the bundled set — never drawn)
node .opencode\skills\python-neon-broll-html\scripts\logos.js python   # -> {"slug":"python","title":"Python","hex":"3776AB",...}
node .opencode\skills\python-neon-broll-html\scripts\logos.js terminal # -> GNU Bash (not used on screen)

# verify + render every scene
cd build\<scene>\hyperframes
npx hyperframes lint; npx hyperframes check
npx hyperframes render -o ..\..\..\renders\<scene>.mp4
```
