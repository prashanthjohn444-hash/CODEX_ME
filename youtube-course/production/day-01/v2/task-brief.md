# Day 1 v2 — shared task brief (Run Your First Python File)

Regeneration of Day 1 with fresh assets. Source of truth: `youtube-course/day-01-spoken-script.md`.
Reference of the previous run: `youtube-course/production/day-01/` (old assets stay untouched; all new work goes under `v2\` subfolders).
Spec: 1920×1080, 30 fps, Rec.709, H.264 MP4, 48 kHz audio. Dark charcoal background, warm yellow labels, restrained blue highlights. Genuine editor recordings only for demos; motion graphics explain relationships, never shown as IDE captures.

## Voice (voice-gen)
- TTS: local VoiceStudio/OmniVoice backend at http://127.0.0.1:3900 (see reference implementation `voice\generate.py`). Voice required: **Adam** — do NOT silently fall back to the old demo voice; if Adam is not available, report the exact voice list and stop.
- Output: `voice\v2\` — one WAV per section, mono 48 kHz PCM16, plus combined `day-01-narration.*` and `manifest.json`.

## Screen capture (screen-capture)
- OBS Studio 1920×1080, isolated profile `Python30Days-Day01`. Captures → `screen\v2\captures\section-NN-obs.mkv`.
- Demo material: `screen\demo\python-30-days\` (hello.py, broken_example.py, printed_expression.py, types_preview.py, expression_only.py).
- Phase A: build profile/scene collection + ONE verified test capture first. Phase B: one capture per section 01–11 following the spoken script's [ON SCREEN] lines: real terminal `python --version`, `>>>` prompt in/out with exit(), typed expressions + print + predictions, deliberate broken parenthesis and repair, hello.py in VS Code run and re-run, type() comparisons. Keep code/output readable at 1080p; verify duration+resolution of each capture; never fabricate captures.

## B-roll (broll-render)
- Skill: python-neon-broll-html. Output: `broll\v2\scenes\*.js` → build `--target all` → HTML + HyperFrames (+ Remotion if clean). Render finished clips to mp4 where the engines reference supports it. Clips ≤ 4.5 s (+0.4 s hold), motion starts ≤ 0.3 s, python logo where the language is the subject.
- Scenes per the narrative edit map (unique graphics; section 09 reuses the section-01 clip):
  1. `shell-vs-file` — compare · paper: shell shows 30, saved file runs and prints nothing → INPUT/MEMORY/OUTPUT framing. (Sections 01, 09)
  2. `setup-path` — flow · neon: setup → shell → file. (Section 02)
  3. `python-uses` — flow · paper: one interpreter → automation / data / web. (Section 03)
  4. `interpreter-flow` — flow · neon: file → python.exe → output. (Section 04)
  5. `prompt-map` — compare · paper: `>>>` vs terminal prompt; exit() returns you. (Section 05)
  6. `syntax-repair` — decision · neon: broken `print("Hello, Python!"` vs repaired line; repaired path must show correct output. (Section 07)
  7. `file-run-cycle` — flow · neon: edit → save → python hello.py → output → change again. (Section 08)
  8. `type-map` — compare · paper: `type(30)` int vs `type('30')` str — same look, different type. (Section 10)
  9. `challenge-card` — paper still-card style scene ≤ 4 s: Day 1 challenge text ("Save and run your own greeting file"), sans logo emphasis. (Section 11)
- Every code line and printed result must be exactly real Python output; escape `<` as `&lt;`.

## Sign-off for all agents
Never present failed work as done. Missing/blocking items are reported explicitly with what you need. Report per-section status tables and real file paths only.
