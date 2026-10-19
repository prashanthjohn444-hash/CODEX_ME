"""Map verified OBS takes and narration sections to a Resolve edit plan.

Source images are never invented or silently substituted. Technical B-roll
appears briefly above genuine screen footage, with audio remaining continuous.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / "voice" / "manifest.json"
SCREEN = ROOT / "screen" / "obs-capture-results.json"
BROLL = ROOT / "broll" / "manifest.json"
OUTPUT = ROOT / "timeline" / "edit-plan.json"
FRAME_RATE = 30


def main():
    voice = json.loads(VOICE.read_text(encoding="utf-8"))
    screen = json.loads(SCREEN.read_text(encoding="utf-8"))
    broll = json.loads(BROLL.read_text(encoding="utf-8"))
    if voice["status"] != "completed" or not screen["status"].startswith("captured"):
        raise RuntimeError("Both voice and OBS screen sections must be complete")
    shots = {capture["section"]: capture for capture in screen["captures"]}
    assert set(shots) == set(range(1, 12))
    broll_by_name = {item["id"]: item for item in broll["clips"]}
    clips = []
    chapters = []
    cursor = 0
    spans = {}
    for section in voice["sections"]:
        number = int(section["id"])
        video = shots[number]
        sound = ROOT / "voice" / section["file"]
        if not sound.is_file():
            raise FileNotFoundError(sound)
        frames = round(section["audio"]["duration_seconds"] * FRAME_RATE)
        if video["duration_seconds"] < section["audio"]["duration_seconds"] + 1:
            raise RuntimeError(f"OBS section {number} is too short to trim its opening")
        clips.append({"kind": "video", "section": number, "path": video["path"],
                      "track": 1, "record_frame": cursor, "source_in_frame": 15,
                      "duration_frames": frames, "source": "actual OBS Studio recording"})
        clips.append({"kind": "audio", "section": number, "path": str(sound),
                      "track": 1, "record_frame": cursor, "source_in_frame": 0,
                      "duration_frames": frames, "source": "synthetic English narration"})
        chapters.append({"frame": cursor, "title": section["title"]})
        spans[number] = {"start": cursor, "duration": frames}
        cursor += frames

    # 1080p motion inserts: B-roll is instructional annotation, never proof.
    placements = [
        ("01-shell-vs-script", 1, 3.5), ("02-execution-flow", 3, 5),
        ("03-python-uses", 3, 16), ("04-prompt-map", 5, 4),
        ("05-syntax-repair", 7, 6), ("06-types-map", 10, 12),
        ("07-exercise-card", 11, 8),
    ]
    for name, section, offset in placements:
        item = broll_by_name[name]
        path = ROOT / "broll" / item["output"]
        if not path.is_file():
            raise FileNotFoundError(path)
        frame = spans[section]["start"] + round(offset * FRAME_RATE)
        max_frame = spans[section]["start"] + spans[section]["duration"]
        frames = min(item["frames"], max_frame - frame)
        if frames <= 0:
            raise RuntimeError(f"B-roll {name} does not fit section {section}")
        clips.append({"kind": "video", "section": section, "path": str(path),
                      "track": 2, "record_frame": frame, "source_in_frame": 0,
                      "duration_frames": frames, "source": "HyperFrames instructional graphic"})

    plan = {"format": "resolve-course-edit-plan/v1", "fps": FRAME_RATE,
            "width": 1920, "height": 1080, "total_frames": cursor,
            "duration_seconds": cursor / FRAME_RATE, "clips": clips, "chapters": chapters,
            "notes": ["Synthetic narration, not a recording of the creator's voice.",
                      "All V1 clips are real OBS captures; V2 contains HyperFrames graphics.",
                      "Review each shot for unintended overlays and verify sync before publishing.",
                      "ChatGPT-generated imagery was not available and was not substituted."]}
    OUTPUT.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(f"Built {len(clips)}-clip edit plan, {cursor} frames / {cursor / FRAME_RATE:.2f}s")


if __name__ == "__main__":
    main()
