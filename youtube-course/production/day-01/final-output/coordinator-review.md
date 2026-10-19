# Day 1 coordinator review

Production started on user instruction, 2026-10-19. Day completion remains pending final Resolve export and full editorial review.

## Current decisions

- Adam narration must match `youtube-course/day-01-spoken-script.md` (SHA-256 `4f926bb322bdf66c3f9371422a84cf20a6ad691b1457856bdc61181c61a695a4`). Matching legacy WAVs may be imported with provenance; signal checks do not establish complete speech or pronunciation.
- Reject `screen/v2/captures/` as genuine screen demonstrations. The screen specialist traced these to `screen/tutorial_generator/generate_all_sections.js`, which uses Puppeteer and generated editor/terminal HTML. Preserve those files, but exclude them from the final lesson's genuine demonstration track.
- The older `output/DELIVERY-REPORT.md` is not acceptance evidence. Its capture claims conflict with the generator provenance. Earlier timeline reports also leave listening, synchronization, installation pickups and Resolve export pending.
- Use dark olive/sage HyperFrames graphics, with illustrative scenes recorded separately from genuine code captures.
- Assembly starts only after audio, screen and required graphics pass their stage checks. A diagnostic FFmpeg video cannot satisfy the Resolve master requirement.

## Review gates

1. Audio: exact script/voice/settings provenance, measured sections/offsets, decoded samples, transcript completeness, listening and pronunciation review.
2. Screen: authentic VS Code/OBS footage, readable correct code/results, installation references, extension/interpreter selection, genuine error/repair and greeting changes, sufficient narration coverage, privacy inspection.
3. Motion: seek-safe editable HyperFrames sources, correct Python, 1080p30 renders, visual inspection, provisional versus verified cue timing distinguished.
4. Assembly: dedicated Resolve project, relinkable media, editable DRP, Resolve-exported MP4, full decode and end-to-end technical/teaching review.

Detailed evidence belongs in each stage's manifest. Existing legacy artifacts remain in place.
