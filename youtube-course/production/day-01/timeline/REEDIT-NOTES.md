# Day 01 revised edit — editorial handoff

This is a **new** version; the previous Resolve project and MP4 remain unchanged.

## What changed

- Voice Studio's English **VENKAT-ENGLISH** profile `73ef31d5` narrates the unchanged spoken script in eleven separate WAVs. See `../voice/reedit-venkat/ALIGNMENT.md` for measured section boundaries and provenance.
- OBS section takes are source-trimmed and gently time-fitted to the new voice. These intermediates remain **genuine OBS footage**, not reconstructed IDE screens; source offsets and speed factors are in `reedit-media/manifest.json`.
- The opening question is led by the real shell/file proof, not an explanatory card that gives away the answer. The shell/script diagram appears once in the later explanation. Uses, prompt, types and challenge graphics appear near their spoken concepts. The file-based syntax-repair card is omitted: it must not stand in for interactive-shell behavior. The premature execution-flow graphic is omitted.
- The final viewing copy is `../output/python-day-01-reedit-review.mp4`, rendered with FFmpeg for review. `reedit-resolve-import.fcpxml` is the editable DaVinci Resolve interchange timeline with V1 OBS-derived footage, V2 technical graphics and A1 Venkat narration. **The viewing copy is not a Resolve export, and XML creation does not prove that Resolve imported it.**

The review copy probes as 1920×1080 H.264 at 30 fps with 48 kHz AAC audio, runtime 385.921 s. A full audio/video stream decode and chapter representative-frame extraction passed; details are in `reedit-verification.json`. DaVinci Resolve was launched, but its external scripting endpoint returned no connection, so **no revised `.drp` or Resolve-rendered master was created**. The existing `.drp` is the earlier version and must not be confused with this cut. Import `reedit-resolve-import.fcpxml` into a new project and inspect relinking before claiming a Resolve delivery.

**Resolve handoff:** in a new 1920×1080, 30 fps project, choose **File → Import → Timeline**, select `reedit-resolve-import.fcpxml`, allow relinking to this Day 1 production folder, verify V1/V2/A1 and 11 chapter sections, then save/export a new `.drp` and H.264 master. Do not overwrite `Python-Day-01-Course.drp` or `python-day-01-english.mp4` (the older cut).

## Important footage limitations

The eleven original OBS takes do **not** show a visit to python.org or the VS Code download page, a real installer, the Python-by-Microsoft extension panel, interpreter selection, creation of a new file, a changed greeting rerun, or a finished challenge. Section 08 therefore still has a long static/editor hold. See `../screen/reedit-screen-audit.md` for missing shots and safe retake instructions. The split-screen described by the hook is represented by sequential actual runs rather than simultaneous footage. Never label explanatory graphics as recordings or claim an installer was filmed.

Before publishing: record the missing pickups in the isolated OBS scene after a privacy check; replace the section 08 holds; check every spoken word against the visual at normal speed; inspect any notifications/history in the source footage; import the XML into Resolve, confirm online media and audio, and export a Resolve master. Automated stream/decode checks alone are not publication approval.
