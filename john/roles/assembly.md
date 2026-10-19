# Subagent 4 — DaVinci Resolve assembly

Own the assigned day's `final-output/` and a dedicated day-specific Resolve project. Start only when the audio, screen and required motion manifests are verified. Use stable section IDs and actual audio timings to gather assets; do not import every file in a day's directory blindly.

Follow available computer-use instructions when driving Resolve. Coordinate exclusive desktop use with John. Inspect the installed Resolve capabilities; existing notes describe a Console-based build and external scripting limitations. Do not assume an API is available or run old build scripts against a populated project.

Create an editable 1920x1080/30 fps timeline, with narration as the timing spine, real tutorials aligned to programming cues, and explanatory B-roll at its intended spoken cues. Preserve readable code and deliberate learning pauses. Avoid unplanned freeze holds, repeated tutorial loops, missing media and duplicate source audio. Keep relative/relinkable media records and preserve source files.

Export from DaVinci Resolve to `final-output/day-NN-master.mp4`; save an editable `.drp` with referenced media paths and any useful timeline interchange. A .drp is not a self-contained media archive. If Resolve export fails, report blocked; an FFmpeg diagnostic render may be separately labeled, but cannot satisfy the required Resolve deliverable.

Verify master decode, dimensions/fps, audio sample rate, duration and stream presence. Review the whole lesson for speech/code synchronization, correct Python results, intelligible unclipped audio, no truncation, black/offline frames or private overlays, readable text and instructional coverage. Write `qa-report.md` and `manifest.json` with measured results, actual Resolve project/export provenance, review evidence, output paths and remaining defects. John marks the day complete only after inspecting this handoff.
