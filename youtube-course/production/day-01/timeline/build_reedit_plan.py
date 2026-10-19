"""Build a separate, sentence-aware Day 1 edit from verified Venkat narration.

Technical graphics only appear after the relevant concept is introduced. The
script refuses to fall back to the earlier demo voice and uses separately
documented OBS retimes instead of pretending they are new shots.
"""
import json
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / "voice" / "reedit-venkat" / "manifest.json"
FITTED = ROOT / "timeline" / "reedit-media" / "manifest.json"
GRAPHICS = ROOT / "broll" / "manifest.json"
OUTPUT = ROOT / "timeline" / "reedit-plan.json"
FPS = 30

# Relative positions were reviewed against the original section lengths.
# Preserve roughly the same spoken phrase when a replacement voice changes pace.
ORIGINAL_SECONDS = [12.470, 13.528, 30.809, 39.335, 33.203, 29.857,
                    34.158, 75.860, 34.523, 36.682, 17.634]
PLACEMENTS = [
    ("03-python-uses", 3, 8.0),
    ("04-prompt-map", 5, 26.0),
    ("01-shell-vs-script", 9, 10.0),
    ("06-types-map", 10, 10.0),
    ("07-exercise-card", 11, 13.0),
]


def audio_seconds(path):
    with wave.open(str(path), "rb") as handle:
        assert handle.getframerate() == 48000
        return handle.getnframes() / handle.getframerate()


def main():
    voice = json.loads(VOICE.read_text(encoding="utf-8"))
    if voice.get("status") != "completed" or voice.get("voice_name", "").lower() != "venkat-english":
        raise RuntimeError("A completed Voice Studio venkat-English manifest is required; no demo-voice fallback")
    screen = json.loads(FITTED.read_text(encoding="utf-8"))
    broll = json.loads(GRAPHICS.read_text(encoding="utf-8"))
    shots = {c["section"]: c for c in screen["sections"]}
    graphics = {c["id"]: c for c in broll["clips"]}
    clips, chapters, section_frames = [], [], {}
    cursor = 0
    for section in voice["sections"]:
        number = int(section["id"])
        sound = VOICE.parent / section["file"]
        duration = audio_seconds(sound)
        frames = round(duration * FPS)
        shot = shots[number]
        if shot["frames"] != frames:
            raise RuntimeError(f"Section {number:02d} fitted video differs from narration by frames")
        clips.append({"kind": "video", "section": number, "path": shot["output"], "track": 1,
                      "record_frame": cursor, "source_in_frame": 0, "duration_frames": frames,
                      "source": "real OBS screen capture, time-fitted; see reedit-media/manifest.json"})
        clips.append({"kind": "audio", "section": number, "path": str(sound.resolve()), "track": 1,
                      "record_frame": cursor, "source_in_frame": 0, "duration_frames": frames,
                      "source": "Voice Studio venkat-English narration"})
        chapters.append({"frame": cursor, "title": section["title"]})
        section_frames[number] = (cursor, frames)
        cursor += frames
    if set(section_frames) != set(range(1, 12)):
        raise RuntimeError("All eleven narration sections are required")
    for name, section, offset in PLACEMENTS:
        item = graphics[name]
        path = ROOT / "broll" / item["output"]
        if not path.is_file():
            raise FileNotFoundError(path)
        start, length = section_frames[section]
        relative = round(offset * (length / FPS) / ORIGINAL_SECONDS[section - 1] * FPS)
        relative = min(relative, length - item["frames"])
        if relative < 0:
            raise RuntimeError(f"Graphic {name} cannot fit narration section {section}")
        clips.append({"kind": "video", "section": section, "path": str(path.resolve()), "track": 2,
                      "record_frame": start + relative, "source_in_frame": 0,
                      "duration_frames": item["frames"], "source": "silent HyperFrames technical explanation"})
    plan = {"format": "resolve-course-reedit-plan/v1", "fps": FPS, "width": 1920, "height": 1080,
            "total_frames": cursor, "duration_seconds": cursor / FPS, "clips": clips, "chapters": chapters,
            "notes": ["Narration must be Voice Studio venkat-English; no substitution.",
                      "05 syntax-repair graphic omitted: saved-file error cannot stand in for shell input.",
                      "02 execution-flow graphic omitted: it anticipates the actual file demonstration.",
                      "OBS footage retimed to fit new voice without inventing UI actions; see reedit-media/manifest.json.",
                      "Uncaptured installation, extension, selected interpreter, and greeting-change shots remain gaps.",
                      "Review scaled graphic slots against audible words before publication."]}
    OUTPUT.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(f"Re-edit plan: {len(clips)} clips, {cursor / FPS:.2f}s; {OUTPUT}")


if __name__ == "__main__":
    main()
