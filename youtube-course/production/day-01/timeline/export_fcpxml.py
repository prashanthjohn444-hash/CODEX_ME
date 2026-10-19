"""Prepare a Final Cut XML interchange timeline for import into DaVinci Resolve.

This is an interchange file, not a claim that it has already been opened or
rendered by Resolve. OBS V1, narration A1, and HyperFrames V2 stay editable.
"""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
PLAN = ROOT / "edit-plan.json"
OUTPUT = ROOT / "day-01-resolve-import.fcpxml"


def time(frames):
    return f"{frames}/30s" if frames else "0s"


def uri(path):
    return Path(path).resolve().as_uri()


def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    if plan["fps"] != 30:
        raise ValueError("Only the verified 30 fps plan can be exported")
    sources = json.loads((ROOT.parent / "screen" / "obs-capture-results.json").read_text(encoding="utf-8"))
    graphics = json.loads((ROOT.parent / "broll" / "manifest.json").read_text(encoding="utf-8"))
    lengths = {c["path"]: round(c["duration_seconds"] * 30) for c in sources["captures"]}
    lengths.update({str((ROOT.parent / "broll" / c["output"]).resolve()): c["frames"] for c in graphics["clips"]})
    lengths.update({c["path"]: c["duration_frames"] for c in plan["clips"] if c["kind"] == "audio"})
    root = ET.Element("fcpxml", version="1.10")
    resources = ET.SubElement(root, "resources")
    ET.SubElement(resources, "format", id="f1", name="FFVideoFormat1080p30", frameDuration="1/30s",
                  width="1920", height="1080", colorSpace="1-1-1 (Rec. 709)")
    paths = {}
    for index, clip in enumerate(plan["clips"], 2):
        path = clip["path"]
        if path in paths:
            continue
        ref = f"r{index}"
        paths[path] = ref
        media = {"id": ref, "name": Path(path).name, "src": uri(path), "start": "0s",
                 "duration": time(lengths[path]),
                 "format": "f1", "hasVideo": "1" if clip["kind"] == "video" else "0",
                 "hasAudio": "1" if clip["kind"] == "audio" else "0"}
        if clip["kind"] == "audio":
            media.pop("format")
            media["audioSources"] = "1"
            media["audioChannels"] = "1"
        ET.SubElement(resources, "asset", media)
    library = ET.SubElement(root, "library")
    event = ET.SubElement(library, "event", name="Python 30 Days")
    project = ET.SubElement(event, "project", name="Day 01 — English lesson")
    sequence = ET.SubElement(project, "sequence", format="f1", duration=time(plan["total_frames"]),
                             tcStart="0s", tcFormat="NDF", audioLayout="stereo", audioRate="48k")
    spine = ET.SubElement(sequence, "spine")
    videos = sorted((c for c in plan["clips"] if c["kind"] == "video" and c["track"] == 1),
                    key=lambda c: c["record_frame"])
    overlays = [c for c in plan["clips"] if c["kind"] == "video" and c["track"] == 2]
    voices = {c["section"]: c for c in plan["clips"] if c["kind"] == "audio"}
    by_section = {}
    for item in overlays:
        by_section.setdefault(item["section"], []).append(item)
    for video in videos:
        section = video["section"]
        base = ET.SubElement(spine, "asset-clip", ref=paths[video["path"]],
                             name=f"Section {section:02d} — OBS VS Code",
                             offset=time(video["record_frame"]),
                             start=time(video["source_in_frame"]), duration=time(video["duration_frames"]),
                             audioRole="dialogue")
        voice = voices[section]
        ET.SubElement(base, "asset-clip", ref=paths[voice["path"]],
                      name=f"Section {section:02d} — English narrator",
                      lane="-1", offset="0s", start="0s", duration=time(voice["duration_frames"]),
                      role="dialogue")
        for overlay in by_section.get(section, []):
            local = overlay["record_frame"] - video["record_frame"]
            ET.SubElement(base, "asset-clip", ref=paths[overlay["path"]],
                          name=Path(overlay["path"]).stem, lane="1", offset=time(local),
                          start=time(overlay["source_in_frame"]),
                          duration=time(overlay["duration_frames"]))
    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
    ET.parse(OUTPUT)
    print(f"Created XML for Resolve: {OUTPUT} ({len(videos)} OBS + {len(overlays)} B-roll + {len(voices)} audio)")


if __name__ == "__main__":
    main()
