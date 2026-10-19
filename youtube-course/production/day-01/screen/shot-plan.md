# Day 1 genuine OBS + VS Code screen-capture plan

**Current plan:** The user explicitly approved VS Code instead of the unavailable Astra IDE and requested OBS Studio for recording. OBS 32.2.2 and VS Code are installed. A project-specific OBS collection captures the primary 1920×1080 display at 30 fps; a test MKV frame was inspected and shows real VS Code editor and Python terminal output. Numbered lesson takes are verified in `obs-capture-results.json` after recording. Do not represent animated B-roll as recorded code. Do not alter the installed Python interpreter for the tutorial.

## Capture prerequisites

1. Use the separately named OBS **Python30Days-Day01** profile and scene collection. Select the physical primary display in source Properties; `monitor: 0` alone produced a black diagnostic test. Inspect a real recorded frame before marking captures valid.
2. Open the isolated VS Code profile at `demo/python-30-days`. Keep filename, terminal cwd, interpreter, and `>>>` prompt in frame. Record real edits and executions, not generated terminal imagery. Save silent, independently numbered MKV takes at 1920×1080/30 fps.
3. Use `python --version` and the actual version shown, not a fabricated installer sequence. Record a separate official download/extension view if the section 08 editor setup narration requires it; actual `hello.py` runs remain the main evidence.

## Shots (identifiers follow spoken-script sections)

| ID | Demonstration to capture in genuine IDE / terminal | Expected result / edit note |
| --- | --- | --- |
| S01-hook-shell-file | In real Python shell enter `10 + 20` → `30`; at terminal run `python expression_only.py` → no output; then run `python printed_expression.py` → `30`. | Keep terminal prompt and `>>>` distinct; reframe in edit for contrast. |
| S02-destination | Open `hello.py`, run `python hello.py`. | `Hello, Python!` then `30`; leave code/output visible. |
| S03-use-cases | Hold working file while narration mentions automation, data, web. | No fabricated IDE overlays required. |
| S04-version | In actual terminal run `python --version`. | Capture installed version, without changing Python installation. |
| S05-prompts | In terminal run `python`; show `>>>`; enter `exit()`; return to terminal; start Python once more, then leave with `exit()`. | Preserve prompt transitions; do not type `python hello.py` inside `>>>`. |
| S06-expressions | At `>>>`: `10 + 20`, `10 - 3`, `4 * 5`, `print("Hello, Python!")`; change greeting and repeat. | Outputs `30`, `7`, `20`, `Hello, Python!`; shell display versus `print` visible. |
| S07-repair | In VS Code open `broken_example.py`, run from terminal; show actual syntax error; add `)` and rerun. | Same editor/terminal context; corrected result `Hello, Python!`. Reset demo file to broken state before any retake if necessary. |
| S08-hello-file | Show actual VS Code editor, `hello.py`, correct folder, `python hello.py`; supplement with official installer/extension view if needed. | Script specifically names VS Code and its Microsoft Python extension; the run must be genuine. |
| S09-resolve | Run `expression_only.py`, compare Python shell `10 + 20`, then run `printed_expression.py`. | File emits nothing until `print(...)` is present. |
| S10-types | Open and run `types_preview.py`. | `<class 'int'>`, `<class 'float'>`, `<class 'str'>`, `<class 'bool'>`; comment produces no output. |
| S11-challenge | Leave challenge uncompleted, show file creation task and Day 1 exercises only if available. | No solution on screen; pause point for viewer. |

The separate `broken_example.py` exists solely to reproduce the error; do not run it as part of normal success demonstrations. Capture installation/web pages only if actually visited and accurately represented. Each video shot must be checked before assigning a duration and changing its manifest status to `captured`.
