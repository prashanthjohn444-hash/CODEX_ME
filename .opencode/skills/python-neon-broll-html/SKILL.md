---
name: python-neon-broll-html
description: Build short (under 5 s) animated B-roll for Python and developer-education videos from one scene file, adapting the layout and theme (neon, paper, terminal) to each topic, exported as a recordable HTML player, a HyperFrames composition, and a Remotion project, with real brand logos (Python, GitHub, YouTube, Instagram, X…) resolved from keywords. Also plans which topics should be animated and which screen-recorded (e.g. a 30-day course). Use whenever the user asks for B-roll, cutaways, motion diagrams, animated explainers, HyperFrames or Remotion graphics for a Python/dev concept (strings, variables, lists, loops, if/else, functions, tokens, tools, platforms) or pastes a script/SRT to storyboard — even if they never say "neon", "HTML", "Remotion" or "logo".
---

# Python B-roll (HTML · HyperFrames · Remotion)

Turn one Python micro-concept into one clip of **under 5 seconds** (default 4.5 s + 0.4 s hold) that teaches by motion, not text. The look adapts to the topic: neon is one of three themes, used only where it fits. One scene file produces all three outputs.

## Workflow
1. **Decide animate or record** (`references/topic-to-visual.md`). Installing, typing, running and debugging are screen-recorded, not animated. For a whole course, start from `references/course-30-days.md`.
2. **One learner outcome** per scene (e.g. "each character in a string has an index starting at 0"). Several concepts = several scenes.
3. **Pick layout and theme** for the topic (tables below).
4. **Find the logos** in the topic and script (see Logos). Add `logo:"python"` etc.
5. **Write `scene.js`** (`const SCENE={...};`) from the closest file in `assets/scenes/`; other concepts in `references/concept-recipes.md`.
6. **Build:** `node scripts/build.js scene.js /mnt/user-data/outputs/<concept> --target all` (many clips: `node scripts/batch.js scenes out --target all`)
   - `html` → `<concept>-broll.html` (player with scrub/speed/hide-controls, for quick preview or screen recording)
   - `hyperframes` → `hyperframes/index.html`; `remotion` → `remotion/` (React project). Details, commands and caveats: `references/engines.md`.
   Default to the target the user named; if they named none, build `all` and say which to use. Pass `--target html|hyperframes|remotion` for one.
7. **Verify the Python**: every code line and printed result must be exactly what Python prints. Escape `<` as `&lt;` in code text.
8. **Deliver**: publish the HTML as an artifact when the user wants to preview it; ZIP the output folder for HyperFrames/Remotion and present it. Reply with the outcome, timeline, exact code labels, and which command to run. State what was and was not verified (see engines.md).

## Layouts and themes
| Learner must see… | `layout` |
|---|---|
| Value stored by position/name (variables, strings, lists, dicts) | `lanes`: INPUT / MEMORY cells / OUTPUT |
| A choice; only one path runs (if/else, try/except) | `decision` |
| Repetition with a counter (for/while) | `loop` |
| Steps passing a value (functions, input→output, import, files, pip) | `flow` |
| What differs between two things (list vs tuple, = vs ==, scope) | `compare` (left/right panels + optional input/result) |

| `theme` | Use for |
|---|---|
| `neon` (default) | how-it-works moments, loops, memory, hooks, chapter openers |
| `paper` | definitions, comparisons, recaps, beginner intros |
| `terminal` | command line, pip/git, tooling cutaways |
Choose by what the lesson shows and how the moment should feel; do not use one layout or theme for everything. Details: `references/topic-to-visual.md`.

## SCENE config
`layout, theme, title, subtitle, logo|logos, input:{label,lines}, output:{label,lines}, steps, duration`, plus `memory:{label,cells:[[text,index],…]}` (lanes), `cond:{text,start}` + `branches:{t,f}` (decision), `nodes:[[label,text]×4]` + `counter:{name,value}` (loop), `nodes:[[label,text]×2–5]` (flow), `left:{label,lines}` + `right:{label,lines}` (compare; ids `bt`,`bf`, lines `a0…`,`b0…`). Text is HTML; `{{logo:slug}}` embeds a logo.
**Steps** `[seconds,"command"]`: the state at time *t* is every step ≤ *t* applied in order (so scrubbing, looping and frame rendering are exact). Commands: `show:id,id` · `hot:1,2` (`hot:` clears) · `lit:id` (`lit:` clears) · `dim:id` · `set:id=text`. IDs: `h pin pmem pout cond bt bf nodes`, lines `l0…`, outputs `o0…`, cells `c0…`, nodes `n0…`, compare lines `a0…`/`b0…`, condition value `cv`. The builder warns about unknown ids, long text and clips over 5 s.

## Logos (use the real mark, keyed off the keyword)
Whenever the topic or narration names a language, tool, library, platform or social network, show its logo: heading badge for the scene's subject (`logo:"python"` for any Python lesson), inline `{{logo:youtube}}` where a brand appears in text. Check with `node scripts/logos.js <keyword>`. If a brand is missing, ask for the official SVG (`assets/logos/custom/<slug>.svg`) or omit it; **never draw a look-alike**. Colour, placement and trademark rules: `references/logos.md`.

## Visual DNA (consistent within a series so cuts match)
- 16:9 (1920×1080), thin rounded outlines, flat 2D, no particles or bloom.
- Colour = role in every theme: green = input/true, violet = memory/process, cyan = output/false (theme-tuned shades). Logos keep brand colours.
- Bebas Neue / Barlow / system mono, with Noto Sans Telugu in every stack; text never below ~1.6cqw.
- Reading order top→bottom or left→right; one change at a time; clear a highlight before the next.

## Motion (readable without audio)
~4.5 s: 0–0.5 s heading and code, 0.5–2.5 s state appears, 2.5–4.2 s the operation runs and the result lands, then a 0.4 s hold. Motion must start by 0.3 s. Keep positions identical between scenes for match cuts.

## Syncing to voiceover
Step time = (time the word is spoken) − (time the clip starts in the edit) − ~0.2 s lead. Keep clips under 5 s; Telugu and English narration run at different speeds, so tie motion to the idea, not to specific words, and render once for both languages. For SRT input, list each beat's start time and write the steps from it.

## Quality gate
- Every element needed for this one concept; Python valid; results correct.
- Scrub to 0 leaves nothing behind; the end frame shows the full result.
- Roles/colours consistent; text legible on a phone; logos correct, undistorted, not hand-drawn.
- Targets built without errors; unresolved-logo warnings addressed.

## Honest limits
Cells/boxes are teaching metaphors (say so for references/memory topics). Timings are suggested unless timestamps were supplied. When typing, installs or debugging are the lesson, recommend a real screen recording and use this as a cutaway.

## Optional outputs (only when asked)
Still prompt ("16:9 dark technical keyframe, near-black #050609… Green INPUT [CODE], Violet MEMORY [STATE], Cyan OUTPUT [RESULT]…"), video-model prompt (locked camera, 1 s end hold, warn that generated lettering and logos may drift; leave text and logos to an overlay), Remotion/HyperFrames spec from `steps`.
