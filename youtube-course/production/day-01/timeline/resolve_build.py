"""Build an asset-driven Resolve timeline and export only this new project.

Run from Resolve's Python console with exec(compile(open(PATH, encoding='utf-8').read(), PATH, 'exec')).
External execution also works when Resolve's documented local scripting is enabled.
The final edit-plan.json is populated only from verified media assets.
"""
import datetime
import json
from pathlib import Path
import traceback

ROOT = Path(r"C:\Users\lms-work\Documents\PY_AUDIO\youtube-course\production\day-01")
PLAN = ROOT / "timeline" / "edit-plan.json"
REPORT = ROOT / "timeline" / "resolve-report.json"


def write_report(report):
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def run(resolve):
    report = {"status": "starting", "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    write_report(report)
    try:
        if resolve is None:
            raise RuntimeError("Resolve scripting is unavailable. Run this script from the application's Python console.")
        if not PLAN.is_file():
            raise RuntimeError("The verified edit plan is not ready yet; no project was modified.")
        plan = json.loads(PLAN.read_text(encoding="utf-8"))
        clips = plan["clips"]
        if not clips:
            raise RuntimeError("The edit plan contains no clips.")
        for clip in clips:
            if not Path(clip["path"]).is_file():
                raise FileNotFoundError(clip["path"])
            if clip["duration_frames"] <= 0 or clip["record_frame"] < 0:
                raise ValueError("Invalid clip bounds")
        manager = resolve.GetProjectManager()
        name = "Python Day 01 - Course"
        project = manager.GetCurrentProject()
        # Only reuse the blank project created for this task. Do not alter a
        # pre-existing project selected by the user in Resolve.
        if project and project.GetName() == "New Project aPython Day 01 - Course1" and project.GetTimelineCount() == 0:
            if not project.SetName(name):
                raise RuntimeError("Resolve could not rename the new blank course project")
        elif project and project.GetName() == name and project.GetTimelineCount() == 0:
            pass
        else:
            raise RuntimeError("Select the empty Day 1 course project; refusing to modify a different project")
        report.update(project=name, product=resolve.GetProductName(), version=resolve.GetVersionString())
        settings = {"timelineResolutionWidth": "1920", "timelineResolutionHeight": "1080",
                    "timelineFrameRate": "30", "timelinePlaybackFrameRate": "30"}
        if hasattr(project, "SetSettings"):
            if not project.SetSettings(settings):
                raise RuntimeError("Resolve rejected project settings")
        else:
            for key, value in settings.items():
                if not project.SetSetting(key, value):
                    raise RuntimeError(f"Resolve rejected {key}")
        pool = project.GetMediaPool()
        imported = {}
        for path in dict.fromkeys(c["path"] for c in clips):
            result = pool.ImportMedia([path])
            if not result:
                raise RuntimeError(f"Resolve could not import {path}")
            imported[path] = result[0]
        timeline = pool.CreateEmptyTimeline("Day 01 - English lesson")
        if not timeline:
            raise RuntimeError("Could not create timeline")
        project.SetCurrentTimeline(timeline)
        timeline.SetStartTimecode("00:00:00:00")
        for kind in ("video", "audio"):
            needed = max((c.get("track", 1) for c in clips if c["kind"] == kind), default=1)
            while timeline.GetTrackCount(kind) < needed:
                if not timeline.AddTrack(kind):
                    raise RuntimeError(f"Could not add {kind} track")
        placed = []
        for clip in clips:
            start = clip.get("source_in_frame", 0)
            info = {"mediaPoolItem": imported[clip["path"]], "startFrame": start,
                    "endFrame": start + clip["duration_frames"] - 1,
                    "recordFrame": clip["record_frame"], "trackIndex": clip.get("track", 1),
                    "mediaType": 1 if clip["kind"] == "video" else 2}
            result = pool.AppendToTimeline([info])
            if not result:
                raise RuntimeError(f"Could not place {clip['path']}")
            placed.append({"path": clip["path"], "record_frame": clip["record_frame"], "kind": clip["kind"]})
        report["placed"] = placed
        for chapter in plan.get("chapters", []):
            timeline.AddMarker(chapter["frame"], "Blue", chapter["title"], "Day 1 lesson section", 1)
        manager.SaveProject()
        archive = ROOT / "timeline" / (name.replace(":", "-") + ".drp")
        report["project_exported"] = bool(manager.ExportProject(name, str(archive)))
        report["project_file"] = str(archive)
        codecs = project.GetRenderCodecs("mp4")
        report["mp4_codecs"] = codecs
        match = next((value for label, value in codecs.items() if "264" in label or "264" in value), None)
        if not match or not project.SetCurrentRenderFormatAndCodec("mp4", match):
            raise RuntimeError("No usable MP4 H.264 encoder was exposed by this Resolve installation.")
        output = ROOT / "output"
        output.mkdir(exist_ok=True)
        project.SetCurrentRenderMode(1)
        render_settings = {"SelectAllFrames": True, "TargetDir": str(output),
                           "CustomName": "python-day-01-english", "ExportVideo": True,
                           "ExportAudio": True, "FormatWidth": 1920, "FormatHeight": 1080,
                           "FrameRate": 30, "VideoQuality": 18000,
                           "AudioCodec": "aac", "AudioSampleRate": 48000,
                           "NetworkOptimization": True}
        if not project.SetRenderSettings(render_settings):
            raise RuntimeError("Resolve rejected render settings")
        job = project.AddRenderJob()
        if not job:
            raise RuntimeError("Resolve could not queue the export")
        report.update(render_job_id=job, status="queued", output_dir=str(output))
        write_report(report)
        if not project.StartRendering([job]):
            raise RuntimeError("Resolve could not start this render job")
        report["status"] = "rendering"
        write_report(report)
        # Return control to Resolve; inspect GetRenderJobStatus(job) after completion.
        print("Created timeline and started render:", name, job)
    except Exception:
        report.update(status="blocked", error=traceback.format_exc())
        write_report(report)
        print(report["error"])


if "resolve" not in globals() or not hasattr(resolve, "GetVersionString"):
    import DaVinciResolveScript as dvr_script
    resolve = dvr_script.scriptapp("Resolve")
run(resolve)
