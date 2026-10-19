# Choosing the treatment for each topic

Decide in this order. Stop at the first match.

1. **Is the lesson the doing?** Installing, typing, running, debugging, reading an error, using an editor/website → **do not animate. Screen-record.** Optional: a 2–3 s terminal-theme cutaway of the result (e.g. `python --version`).
2. **Is it an idea you can't see?** (what a variable is, how a loop repeats, what a function returns) → animate. Pick the layout, then the theme.
3. **Is it a single fact or definition?** Put it as a 1-line title card in the editor; no scene needed.

## Layout by what the learner must see
| Learner must see… | layout | Typical topics |
|---|---|---|
| Value stored and picked out by position/name | `lanes` | variables, strings, lists, dicts, indexing |
| A choice, only one path runs | `decision` | if/elif/else, try/except, comparison results |
| Something repeating, a counter changing | `loop` | for, while, break/continue, range |
| Steps passing a value along | `flow` | function call, return, input→process→output, import, file read/write, pip, request/response |
| Two things side by side, what differs | `compare` | list vs tuple, = vs ==, for vs comprehension, local vs global, mutable vs immutable |

## Theme by the feeling of the moment
| Theme | Use for | Avoid for |
|---|---|---|
| `neon` (dark, glow) | how-it-works moments, loops, memory, flows; hooks and chapter openers | long reading, comparisons that need calm, anything printed |
| `paper` (light, flat) | definitions, comparisons, recaps, beginner intros, anything viewers may screenshot or print | night-style hype moments |
| `terminal` (black/green mono) | command line, pip/git/venv, tooling cutaways | concepts that aren't about a command |
Use one theme per day's clips, and `paper` for every recap so recaps feel different from teaching.

## Clip budget (under 5 s)
~4.5 s + 0.4 s hold. One idea. ≤3 code lines (decision ≤5, loop ≤4 inputs), ≤3 on-screen text blocks, title ≤22 characters. `node scripts/build.js` warns about all of these.
Plan 3–5 clips a day: hook (neon, 2–3 s), 1–2 concept clips, optional compare, recap (paper).

## Telugu + English
Render each clip once; dub in either language. Keep Python code, titles and logos in English (they are the same in both versions). If a Telugu label is wanted, use one or two words in `subtitle` and install Noto Sans Telugu (it is already in every font stack).
