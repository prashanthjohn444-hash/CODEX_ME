# Day 1 VENKAT-ENGLISH narration — alignment evidence

- **Source:** `youtube-course/day-01-spoken-script.md`; SHA-256 `4f926bb322bdf66c3f9371422a84cf20a6ad691b1457856bdc61181c61a695a4`, identical to the original `voice/manifest.json` source. The 11 spoken section texts match the original manifest exactly.
- **Voice:** Live local Voice Studio `/profiles` and `/v1/audio/voices` listed English profile `73ef31d5` (`VENKAT-ENGLISH`). `/audiobook/plan` assigned all 11 chapters to that ID; the completed `/audiobook` response reports the rendered voice as `73ef31d5` / `VENKAT-ENGLISH`. Synthetic cloned narration, not a human recording of the full lesson.
- **Outputs:** `day-01-narration.m4b`, `day-01-narration.wav`, `section-01.wav` through `section-11.wav`. The WAV is 48 kHz, mono, 16-bit PCM, **385.920 s**; SHA-256 `eb60ca30a3494ba6f76dba3dbd5b90af3e7647e9860d8e726097ac2a68e1daad`. All 11 section frame counts sum to the full WAV frame count (18,524,160). `manifest.json` retains the request, Voice Studio events, exact text, frame-based intervals, and chapter render reports.

| Section | Start (s) | End (s) | Duration (s) |
| --- | ---: | ---: | ---: |
| 01 Hook | 0.000 | 13.274 | 13.274 |
| 02 Turn | 13.274 | 27.990 | 14.716 |
| 03 What Python does | 27.990 | 61.560 | 33.570 |
| 04 Verify interpreter | 61.560 | 103.926 | 42.366 |
| 05 Know the prompt | 103.926 | 138.319 | 34.393 |
| 06 Expressions and text | 138.319 | 170.801 | 32.482 |
| 07 Break and recover | 170.801 | 207.421 | 36.620 |
| 08 Save and run file | 207.421 | 289.821 | 82.400 |
| 09 Resolve puzzle | 289.821 | 326.904 | 37.083 |
| 10 Types and comments | 326.904 | 366.458 | 39.554 |
| 11 Challenge | 366.458 | 385.920 | 19.462 |

These are **chapter-level** boundaries derived from Voice Studio chapter events (millisecond-rounded), sliced against the decoded WAV's actual sample count; the final chapter absorbs the decoder's remaining frames. They are **not** word-level forced alignment or an independent transcription/accuracy assessment. The previous demo-voice WAV was 358.0587 s; this take is **27.8613 s longer** and has different section boundaries. The existing edit, screen captures and B-roll were not changed; this audio must be re-synced before use in a finished video.
