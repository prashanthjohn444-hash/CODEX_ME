# Day 1 video production status

This directory contains the real capture and editing work for the confirmed English Day 1 pilot.

| Component | Path | Status / provenance |
| --- | --- | --- |
| Narration | `voice/day-01-narration.wav` and eleven `voice/section-NN.wav` files | Complete, local VoiceStudio synthetic English demo voice, 48 kHz mono, about 358 seconds. Not human-recorded. |
| Technical B-roll | `broll/renders/*.mp4` | Seven completed HyperFrames clips, 1920×1080 30 fps. Illustrated explanations, not footage of working Python. |
| OBS screen capture | `screen/captures/section-NN-obs.mkv` | Check `screen/obs-capture-results.json` for completed sections. The OBS profile is isolated and the VS Code footage is authentic. |
| Resolve timeline | `timeline/Python-Day-01-Course.drp` | Editable Resolve project **Python Day 01 - Course**, with 11 OBS clips on V1, seven HyperFrames clips on V2 and separate narration on A1. Source media remains in this directory. |
| FFmpeg review copy | `output/python-day-01-review-ffmpeg.mp4` | 358.09 seconds, H.264/AAC 1920×1080 30 fps; not a Resolve export. |
| Resolve deliverable | `output/python-day-01-english.mp4` | Completed 358.57-second H.264/AAC 1920×1080, 30 fps export. Resolve's H.264 Master Quick Export wrote `python-day-01-english.mp4.mov`; it was losslessly remuxed to `.mp4`. Full stream decoding and automatic checks pass. |

OBS source settings are under a separately named **Python30Days-Day01** scene collection and profile. Existing OBS scenes have not been overwritten. Start with [the OBS notes](screen/OBS-README.md). HyperFrames is pinned to the official HeyGen package in `broll/package.json`, and its creation skills were installed into the user's OpenCode-compatible skill directories. A `hyperframes doctor` check reports FFmpeg missing from system PATH, but the B-roll build uses its own project-local `ffmpeg-static`/`ffprobe-static` binaries. HyperFrames usage reporting returned `status: unknown (unsupported_harness)`; this is not a usage allowance claim.

After the OBS manifest shows eleven verified takes:

```powershell
python youtube-course/production/day-01/timeline/build_edit_plan.py
python youtube-course/production/day-01/timeline/export_fcpxml.py
```

The imported Resolve project is named **Python Day 01 - Course** and the editable timeline is named **Day 01 — English lesson**. It was imported through **File → Import → Timeline** from `timeline/day-01-resolve-import.fcpxml`, with automatic media relinking and 1920×1080/30 fps timeline settings. Resolve's external Python API did not connect in this installation, so the prepared `timeline/resolve_build.py`/`resolve-internal.lua` scripts are not the provenance of this timeline. Do not run them on the populated project. The video export used Resolve's H.264 Master Quick Export. The original Resolve MOV is retained alongside the MP4 copy; `timeline/final-verification.json` records the MP4 probe and representative frame paths.

Review the final export against [the production brief](production-brief.md). Do not publish with unreviewed capture overlays, missing application footage, wrong audio, black frames, or offline Resolve media. ChatGPT illustrative images remain ungenerated; the seven HyperFrames pieces cover the technical motion requirements without pretending to be ChatGPT imagery.

## Review observations

- The FFmpeg review copy has H.264 1920×1080 at 30 fps plus 48 kHz AAC mono narration, with approximately −19.4 dB average and −0.4 dB peak audio levels. The Resolve export has 48 kHz stereo AAC at roughly −22.4 dB mean, −3.2 dB maximum, and no detected silences longer than three seconds below −40 dB. It is independently verified by `timeline/verify_final.py` and decodes without FFmpeg errors.
- The correction shot around 02:57 visibly shows both the earlier `SyntaxError` and the saved corrected code with successful `Hello, Python!` output; the full-size frame is `output/review-repair-actual.png`.
- The opening graphic at about 00:05 is clearly an illustrated HyperFrames explainer, distinct from the real VS Code proof shots.
- The editor-installation portion of the script is supported by VS Code demonstration footage, **not** a recorded VS Code installation walkthrough or genuine browser visit to the extension page. These setup directions require supplemental footage if the video is to match them literally.
