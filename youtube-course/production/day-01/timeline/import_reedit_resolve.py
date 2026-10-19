"""Import the revised plan as a NEW DaVinci Resolve project, if scripting works.

Never changes or renames the previous course project. The FCPXML is the
portable fallback when this installation denies external scripting.
"""
import datetime
import json
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "timeline" / "reedit-plan.json"
REPORT = ROOT / "timeline" / "reedit-resolve-report.json"
NAME = "Python Day 01 - Venkat Reedit"
MODULES = Path(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
sys.path.insert(0, str(MODULES))


def save(data):
    REPORT.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main():
    report = {"project": NAME, "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        import DaVinciResolveScript as dvr
        resolve = dvr.scriptapp("Resolve")
        if not resolve:
            raise RuntimeError("Resolve external scripting did not connect; use reedit-resolve-import.fcpxml")
        manager = resolve.GetProjectManager()
        if manager.LoadProject(NAME):
            raise RuntimeError("A project of this name exists; refusing to overwrite it")
        project = manager.CreateProject(NAME)
        if not project:
            raise RuntimeError("Could not create new Resolve project")
        report.update(status="created", resolve_version=resolve.GetVersionString())
        save(report)
        for key, value in {"timelineResolutionWidth": "1920", "timelineResolutionHeight": "1080",
                           "timelineFrameRate": "30", "timelinePlaybackFrameRate": "30"}.items():
            if not project.SetSetting(key, value):
                raise RuntimeError(f"Resolve rejected project setting {key}={value}")
        plan = json.loads(PLAN.read_text(encoding="utf-8"))
        clips = plan["clips"]
        for clip in clips:
            if not Path(clip["path"]).is_file():
                raise FileNotFoundError(clip["path"])
        pool = project.GetMediaPool()
        imported = {}
        for path in dict.fromkeys(c["path"] for c in clips):
            media = pool.ImportMedia([path])
            if not media:
                raise RuntimeError(f"Resolve could not import {path}")
            imported[path] = media[0]
        timeline = pool.CreateEmptyTimeline("Day 01 - English Venkat re-edit")
        if not timeline or not project.SetCurrentTimeline(timeline):
            raise RuntimeError("Resolve could not create/select timeline")
        timeline.SetStartTimecode("00:00:00:00")
        while timeline.GetTrackCount("video") < 2:
            if not timeline.AddTrack("video"):
                raise RuntimeError("Cannot create technical B-roll track")
        while timeline.GetTrackCount("audio") < 1:
            if not timeline.AddTrack("audio"):
                raise RuntimeError("Cannot create narration track")
        for clip in clips:
            start = clip["source_in_frame"]
            info = {"mediaPoolItem": imported[clip["path"]], "startFrame": start,
                    "endFrame": start + clip["duration_frames"] - 1,
                    "recordFrame": clip["record_frame"], "trackIndex": clip["track"],
                    "mediaType": 1 if clip["kind"] == "video" else 2}
            if not pool.AppendToTimeline([info]):
                raise RuntimeError(f"Could not place {Path(clip['path']).name} at {clip['record_frame']}")
        for chapter in plan["chapters"]:
            timeline.AddMarker(chapter["frame"], "Blue", chapter["title"], "Day 1", 1)
        if not manager.SaveProject():
            raise RuntimeError("Resolve could not save project")
        archive = ROOT / "timeline" / "Python-Day-01-Venkat-Reedit.drp"
        if not manager.ExportProject(NAME, str(archive)) or not archive.is_file():
            raise RuntimeError("Resolve could not export revised project archive")
        report.update(status="exported", clips=len(clips), timeline=timeline.GetName(),
                      archive=str(archive), bytes=archive.stat().st_size)
        save(report)
        print(json.dumps(report, indent=2))
    except Exception:
        report.update(status="blocked", error=traceback.format_exc())
        save(report)
        print(report["error"])
        raise


if __name__ == "__main__":
    main()
