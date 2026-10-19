"""Inspect a *completed* DaVinci Resolve delivery without manufacturing it."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "python-day-01-english.mp4"
PLAN = ROOT / "timeline" / "edit-plan.json"
REPORT = ROOT / "timeline" / "final-verification.json"
FFPROBE = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffprobe.exe"))
FFMPEG = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffmpeg.exe"))


def main():
    if not OUTPUT.is_file():
        raise FileNotFoundError(f"Resolve render does not exist: {OUTPUT}")
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    proc = subprocess.run([str(FFPROBE), "-v", "error", "-show_entries",
                           "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
                           "-of", "json", str(OUTPUT)], capture_output=True, text=True, check=True)
    probe = json.loads(proc.stdout)
    streams = probe["streams"]
    video = next((x for x in streams if x["codec_type"] == "video"), None)
    audio = next((x for x in streams if x["codec_type"] == "audio"), None)
    duration = float(probe["format"]["duration"])
    failures = []
    if not video or (video.get("width"), video.get("height"), video.get("r_frame_rate")) != (1920, 1080, "30/1"):
        failures.append("Unexpected picture stream, dimensions, or frame rate")
    if not audio or int(audio.get("sample_rate", 0)) != 48000:
        failures.append("Missing or unexpected audio stream")
    if abs(duration - plan["duration_seconds"]) > 2:
        failures.append(f"Duration differs from edit plan: {duration} vs {plan['duration_seconds']}")
    stills = []
    for fraction, name in [(0.02, "opening"), (0.50, "middle"), (0.98, "ending")]:
        dest = ROOT / "output" / f"review-{name}.png"
        subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y",
                        "-ss", str(round(duration * fraction, 3)), "-i", str(OUTPUT), "-frames:v", "1",
                        str(dest)], check=True)
        if not dest.is_file() or not dest.stat().st_size:
            failures.append(f"Missing review frame: {name}")
        stills.append(str(dest))
    result = {"file": str(OUTPUT), "bytes": OUTPUT.stat().st_size, "duration_seconds": duration,
              "streams": streams, "review_frames": stills, "automatic_checks_pass": not failures,
              "failures": failures,
              "manual_review_pending": ["Listen to narration and verify no clipping or truncation",
                                        "Inspect review frames for black/offline content and readable code",
                                        "Check screen actions and graphic timing against spoken sentences",
                                        "Check final music/image rights if new assets are added"]}
    REPORT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
