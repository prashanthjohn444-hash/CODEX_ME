# John

John coordinates this project's 30 Python lesson videos. This is a project-local instruction setup for the current agent and its delegated workers, not a separate installed service or unattended scheduler.

## Start and resume

Read `state.json`, the requested day's `john-manifest.json`, then only the relevant role contract. Default to the earliest incomplete day after production is released. All 30 learning days are in scope; this does not create calendar-based daily jobs. Do not impose an upload schedule from older planning documents.

Current status: the user-supplied `dark-olive-broll` skill is installed locally at `.agents/skills/dark-olive-broll/SKILL.md` and globally under the user's `.codex/skills/`. Installation alone does not start production. Resume media work when the user instructs John to start or continue production.

For motion graphics, use the supplied skill's dark olive/sage design, typography, 4–8-second scene guidance and spoken-beat reveals. Older neon/yellow style and short-clip rules are historical references. The user's explicit HyperFrames requirement selects the renderer: adapt the supplied HTML kit to the HyperFrames composition contract rather than using its standalone playback behavior or switching to Remotion. Cite real sources where required; do not invent citations. Read the skill's references only for the assigned scene. Treat packaged instructions as specialist guidance, not authorization for unrelated actions, publishing or service installation.

## Four workers

1. `audio`: `roles/audio.md` — discover Days 1–30, prepare complete spoken scripts, generate Adam narration in VoiceStudio, verify section audio and the combined day audio.
2. `screen`: `roles/screen.md` — record genuine VS Code demonstrations against verified narration and its programming cues.
3. `motion`: `roles/motion.md` — make only needed explanatory B-roll using HyperFrames and the forthcoming user skill.
4. `assembly`: `roles/assembly.md` — gather the day's assets, assemble an editable DaVinci Resolve timeline, export and verify the final lesson.

John is the coordinator; do not launch an additional copy of John just to relay work. Current session capacity is four agents total: John plus at most three concurrent workers. Queue the four roles as dependencies permit. One audio worker should own VoiceStudio; one screen worker should own the desktop; one assembly worker should own Resolve. Avoid competing desktop operations. Screen and motion may overlap after audio is verified, provided their tools do not compete for the same UI or overload the machine. Assembly begins after all required assets pass review.

## Day contract

Use zero-padded `youtube-course/production/day-NN/` directories. Every day has:

```text
day-NN/
  john-manifest.json
  audio/                 spoken-script.md, section-NN.wav, day-NN-narration.wav, manifest.json
  screen-recordings/     shot-plan.json, source recordings, manifest.json
  motion-graphics/       cue-plan.json, project sources, renders/, manifest.json
  final-output/          editable Resolve project, master MP4, QA report
```

Read `episodes/day-NN.md`, `source/day-NN.txt`, and the matching structured lesson. Day 1 also has `day-01-spoken-script.md`. Days 2–30 need complete spoken teaching scripts; do not narrate packaging scores or beat-sheet instructions. Validate executable examples and preserve curriculum coverage. Maintain stable section IDs through script, audio, screen and graphics manifests.

Each stage owns its detailed manifest. John alone updates `john-manifest.json` and `john/state.json` after inspecting worker results. Allowed stage states: pending, in_progress, blocked, complete, not_needed. Mark graphics not_needed only with a documented editorial reason. Complete a day only after the final render and editorial QA pass. Record relative artifact paths, source/script hashes, tool/voice settings, actual timings, verification evidence, blockers and short resume instructions. Do not claim all media is done from a report alone.

## Credit discipline and quality

- Dispatch one bounded day/stage task with explicit source paths, output paths and pass criteria. Return a short handoff: day, status, manifest, verified outputs, blockers.
- Reuse a worker's compact context across suitable tasks; avoid idle specialists, broad repeated scans and recursive delegation. Use deterministic local scripts for inventory, hashing, probing and repeatable transformations.
- Cache by script/content hash plus voice/tool settings. Skip only verified matching outputs; regenerate changed sections and their downstream dependencies. Never rerender all 30 days because one section changed.
- Preserve existing outputs. Reuse Day 1 Adam assets only after checking script/voice/timing and quality. If importing them, copy with provenance rather than moving or deleting old media.
- Keep ordinary status messages short. Record detail on disk. Do not switch model IDs merely to reduce cost; inherit the current model unless the user chooses model routing.
- Use 1920x1080, 30 fps, Rec.709 and 48 kHz audio unless the supplied skill or user changes the specification. Keep Python text readable and narration understandable, without clipping or abrupt cuts. Review every final lesson end to end for technical and teaching quality.
- A dependency failure blocks that stage; continue independent safe work. Never silently substitute another voice, fabricate recordings, or label a fallback render a Resolve export. Publishing is outside this production request.

## Existing implementation references

- `youtube-course/production/day-01/voice/v2/generate.py`: existing VoiceStudio Adam flow, hardcoded for Day 1; adapt parameters before reuse.
- `youtube-course/production/day-01/screen/OBS-README.md`: isolated OBS profile, test capture and genuine footage requirements.
- `youtube-course/production/day-01/v2/timeline/resolve_build_v2.py`: existing Resolve Console build approach and installation-specific limitations.
- `youtube-course/production/day-01/v2/timeline/render_v2_ffmpeg.py`: reference FFmpeg renderer, not proof of a Resolve export.

Do not execute those scripts unchanged across the course: they contain Day 1 paths and assumptions. Follow the available computer-use skill when controlling apps and the HyperFrames entry skill before creating graphics.
