# Python 30 Days — YouTube production pack

Built from `C:\Users\lms-work\Downloads\PYTHON_30_DAYS_LAB_WITH_MIND_MAPS_FIXED.html` using all eleven installed YouTube skills.

## Start here

1. [30-video plan](30-video-plan.md) — lesson titles, thumbnail text, learner outcomes, and links to all 30 briefs.
2. [Day 1 spoken script](day-01-spoken-script.md) — a recordable English pilot with code and screen directions.
3. [Production workflow](production-workflow.md) — capacity-based schedule, Shorts, editing, comments, retention, and pre-launch audit.
4. [Public-video research](research/findings.md) — five sourced references and the same-channel sample comparison.
5. [Production tracker](production-tracker.csv) — spreadsheet-ready status for every lesson.
6. [Sol review](sol-review.md) — verification scope, changes, and inputs still required.
7. [Day 1 media production](production/day-01/README.md) — neutral English narration, OBS/VS Code screen takes, HyperFrames technical B-roll, and DaVinci Resolve assembly status.

Each `episodes/day-NN.md` contains a source-linked production brief, ten scored title candidates summarized as the top three, two editorial title options, a thumbnail brief, five scored hooks summarized as the top two, a beat sheet, one Short concept, description/tags/query checks, untimed chapters, and a source-topic coverage checklist.

## What is ready

- 30 lesson-specific video briefs and description drafts.
- 300 title/thumbnail checks and 150 hook score panels in [all-scores.json](scores/all-scores.json).
- One full spoken pilot; Days 2–30 currently have beat sheets.
- 30 Short concepts plus five ranked pilot candidates with [scored replacement openings](scores/short-hook-scores.json).
- A narration-only [pilot word count and 150-wpm estimate](scores/pilot-metrics.json).
- A workflow sized to the confirmed **under-four-hour weekly capacity** and one prioritized pre-launch improvement.

**Confirmed direction:** English narration; one main lesson every two weeks as the baseline, with a three-hour weekly planning budget and optional Shorts. The pilot will establish actual production time.

## What needs your input

- **Existing assets:** anything already recorded or half-made.
- **Voice:** three of your own videos for a personal voice profile.
- **Channel/resources:** channel URL and public lab, playlist, and code links.
- **After recording:** rough/final timestamped transcripts for real cuts, Shorts timecodes, and validated chapters.
- **After publication:** real comments and retention export for measured analysis.

No final footage, timed chapters, actual comment analysis, or measured channel-retention diagnosis is claimed. Title/hook scores are heuristics. The public reference sample is small and historical.

## Rebuild

### Agent model routing

Configured in [`.opencode/opencode.json`](../.opencode/opencode.json):

- All eleven `yt-*` agents: **GPT-5.6 Sol** (`openai/gpt-5.6-sol`).
- Heavy-task agents `build`, `plan`, and `general`: **GPT-6 Sol** (`openai/gpt-6-sol`).
- Lightweight `explore` agent and project fallback: **GPT-5.6 Sol**.

These are agent preferences; an already-running primary session keeps its selected model. Explicit subagent calls for this continuation use the requested model IDs.

### Regenerate the pack

From the workspace root, using Python 3.9+:

```powershell
python youtube-course/extract_course.py
python youtube-course/build_pack.py
python youtube-course/score_pilot.py
```

The first command reads the original HTML without executing its JavaScript. The build command uses `episode_data.json` and the extracted source, then calls the installed scoring functions and `swipe.py`. It rewrites the generated episode briefs, plan, tracker, and scores; edit the source data when changing generated content. The pilot and workflow are hand-authored.

The original uploaded HTML is unchanged. `source/` contains extracted lesson text and structured data for traceability.

```text
Recommended next recording: Day 1 — Run Your First Python File.
Use English and the under-four-hour weekly budget when expanding the remaining beat sheets into spoken scripts.
```

ship it, or change it?
