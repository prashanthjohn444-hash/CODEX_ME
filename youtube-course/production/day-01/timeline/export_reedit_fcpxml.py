"""Export the revised edit as a separate, importable DaVinci Resolve timeline."""
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
PLAN = ROOT / "reedit-plan.json"
OUTPUT = ROOT / "reedit-resolve-import.fcpxml"
FFPROBE = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffprobe.exe"))


def time(frames):
    return f"{frames}/30s" if frames else "0s"


def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    assert plan["fps"] == 30
    root = ET.Element("fcpxml", version="1.10")
    resources = ET.SubElement(root, "resources")
    ET.SubElement(resources, "format", id="f1", name="FFVideoFormat1080p30", frameDuration="1/30s",
                  width="1920", height="1080", colorSpace="1-1-1 (Rec. 709)")
    refs = {}
    for index, clip in enumerate(plan["clips"], 2):
        path = Path(clip["path"]).resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        if str(path) in refs:
            continue
        ref = f"r{index}"
        refs[str(path)] = ref
        probe = json.loads(subprocess.check_output([str(FFPROBE), "-v", "error", "-show_entries",
                         "format=duration", "-of", "json", str(path)], text=True))
        length = round(float(probe["format"]["duration"]) * 30)
        media = {"id": ref, "name": path.name, "src": path.as_uri(), "start": "0s",
                 "duration": time(length), "hasVideo": "1" if clip["kind"] == "video" else "0",
                 "hasAudio": "1" if clip["kind"] == "audio" else "0"}
        if clip["kind"] == "video":
            media["format"] = "f1"
        else:
            media.update(audioSources="1", audioChannels="1")
        ET.SubElement(resources, "asset", media)
    library = ET.SubElement(root, "library")
    event = ET.SubElement(library, "event", name="Python 30 Days")
    project = ET.SubElement(event, "project", name="Day 01 — re-edit")
    sequence = ET.SubElement(project, "sequence", format="f1", duration=time(plan["total_frames"]),
                             tcStart="0s", tcFormat="NDF", audioLayout="stereo", audioRate="48k")
    spine = ET.SubElement(sequence, "spine")
    for video in sorted((c for c in plan["clips"] if c["kind"] == "video" and c["track"] == 1),
                        key=lambda c: c["record_frame"]):
        section = video["section"]
        base = ET.SubElement(spine, "asset-clip", ref=refs[str(Path(video["path"]).resolve())],
                             name=f"Section {section:02d} — OBS source", offset=time(video["record_frame"]),
                             start=time(video["source_in_frame"]), duration=time(video["duration_frames"]))
        audio = next(c for c in plan["clips"] if c["kind"] == "audio" and c["section"] == section)
        ET.SubElement(base, "asset-clip", ref=refs[str(Path(audio["path"]).resolve())],
                      name=f"Section {section:02d} — narration", lane="-1", offset="0s",
                      start=time(audio["source_in_frame"]), duration=time(audio["duration_frames"]), role="dialogue")
        for graphic in (c for c in plan["clips"] if c["kind"] == "video" and c["track"] == 2 and c["section"] == section):
            ET.SubElement(base, "asset-clip", ref=refs[str(Path(graphic["path"]).resolve())],
                          name=Path(graphic["path"]).stem, lane="1",
                          offset=time(graphic["record_frame"] - video["record_frame"]),
                          start=time(graphic["source_in_frame"]), duration=time(graphic["duration_frames"]))
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(OUTPUT, encoding="utf-8", xml_declaration=True)
    ET.parse(OUTPUT)
    print(f"Resolve interchange timeline: {OUTPUT}")


if __name__ == "__main__":
    main()
