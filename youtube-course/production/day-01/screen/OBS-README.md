# OBS Studio capture — Day 1

The **Python30Days-Day01** OBS profile and scene collection are isolated from the user's Untitled setup. Capture is real 1920×1080/30 fps desktop footage of VS Code, not generated graphics. The project-specific demo files live in `demo/python-30-days/`.

## Setup or restore

Run `python setup_obs.py` only if the collection does not already exist. It refuses to overwrite existing OBS settings. Open OBS with this profile and collection, then choose **Properties** on “Display 1 — VS Code demonstration” and select the actual primary display. A display source with only `monitor: 0` may record a black frame until OBS writes the machine-specific `monitor_id`.

Before any batch, record a short MKV test, stop normally, and extract a frame to prove the capture is not black. OBS `--startrecording` alone is not sufficient verification. The first black-source test in `captures/2026-10-09 07-17-13.mkv` is **not** lesson footage; the short functional test in `2026-10-09 07-21-14.mkv` shows the editor but is also not part of the final edit. Keep these as diagnostics.

`capture_obs.py` controls this dedicated OBS collection and isolated VS Code session. It records numbered sections, verifies frame size/rate with ffprobe, and saves `obs-capture-results.json`. It can resume without overwriting a numbered take after an interrupted run. It expects the desktop to remain available for the duration. Do not edit other applications or reveal private windows while full-display capture is active.

The script does not claim frame-perfect speech sync. The DaVinci Resolve timeline will trim and align these source takes to the section WAVs; inspect the transcript and final video before publishing.
