"""One V1 picture + one A1 Venkat narration WAV per chapter, for Resolve."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "timeline" / "premium-media" / "manifest.json"
VOICE = ROOT / "voice" / "reedit-venkat" / "manifest.json"
OUTPUT = ROOT / "timeline" / "premium-day-01.fcpxml"


def tc(frames):
    return f"{frames}/30s" if frames else "0s"


def main():
    pictures = json.loads(SOURCE.read_text(encoding="utf-8"))["chapters"]
    voice = json.loads(VOICE.read_text(encoding="utf-8"))
    if voice["status"] != "completed" or voice["voice_name"].lower() != "venkat-english":
        raise RuntimeError("Completed VENKAT-ENGLISH narration is required")
    if len(pictures) != 11 or len(voice["sections"]) != 11:
        raise RuntimeError("Clean timeline requires all 11 chapters")
    root = ET.Element("fcpxml", version="1.10")
    resources = ET.SubElement(root, "resources")
    ET.SubElement(resources, "format", id="f1", name="FFVideoFormat1080p30", frameDuration="1/30s",
                  width="1920", height="1080", colorSpace="1-1-1 (Rec. 709)")
    for index, picture in enumerate(pictures, 1):
        if picture["section"] != index:
            raise RuntimeError("Picture order is not sequential")
        video = Path(picture["file"])
        audio = ROOT / "voice" / "reedit-venkat" / f"section-{index:02d}.wav"
        if not video.is_file() or not audio.is_file():
            raise FileNotFoundError(video if not video.is_file() else audio)
        if picture["frames"] != round(voice["sections"][index - 1]["audio"]["duration_seconds"] * 30):
            raise RuntimeError(f"Chapter {index:02d} picture/voice frame mismatch")
        ET.SubElement(resources, "asset", id=f"v{index}", name=video.name, src=video.resolve().as_uri(),
                      start="0s", duration=tc(picture["frames"]), format="f1", hasVideo="1", hasAudio="0")
        ET.SubElement(resources, "asset", id=f"a{index}", name=audio.name, src=audio.resolve().as_uri(),
                      start="0s", duration=tc(picture["frames"]), hasVideo="0", hasAudio="1",
                      audioSources="1", audioChannels="1")
    library = ET.SubElement(root, "library")
    event = ET.SubElement(library, "event", name="Python 30 Days")
    project = ET.SubElement(event, "project", name="Day 01 - Premium White Grid")
    total = sum(p["frames"] for p in pictures)
    sequence = ET.SubElement(project, "sequence", format="f1", duration=tc(total), tcStart="0s",
                             tcFormat="NDF", audioLayout="stereo", audioRate="48k")
    spine = ET.SubElement(sequence, "spine")
    cursor = 0
    for index, picture in enumerate(pictures, 1):
        length = picture["frames"]
        clip = ET.SubElement(spine, "asset-clip", ref=f"v{index}", name=f"{index:02d} / picture",
                             offset=tc(cursor), start="0s", duration=tc(length))
        ET.SubElement(clip, "asset-clip", ref=f"a{index}", name=f"{index:02d} / Venkat narration",
                      lane="-1", offset="0s", start="0s", duration=tc(length), role="dialogue")
        cursor += length
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(OUTPUT, encoding="utf-8", xml_declaration=True)
    ET.parse(OUTPUT)
    print(f"Resolve interchange: 11 V1 pictures + 11 A1 narration files, {total} frames: {OUTPUT}")


if __name__ == "__main__":
    main()
