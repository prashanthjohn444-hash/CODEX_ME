"""Automated review-copy QC; never claims a Resolve export or manual sync review."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "python-day-01-reedit-review.mp4"
PLAN = ROOT / "timeline" / "reedit-plan.json"
REPORT = ROOT / "timeline" / "reedit-verification.json"
TOOLS = Path.home() / "AppData/Roaming/OmniVoice/media_tools"
FFMPEG = next(TOOLS.rglob("ffmpeg.exe"))
FFPROBE = next(TOOLS.rglob("ffprobe.exe"))


def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    probe = json.loads(subprocess.check_output([str(FFPROBE), "-v", "error", "-show_entries",
                 "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
                 "-of", "json", str(OUTPUT)], text=True))
    v = next((s for s in probe["streams"] if s["codec_type"] == "video"), {})
    a = next((s for s in probe["streams"] if s["codec_type"] == "audio"), {})
    duration = float(probe["format"]["duration"])
    errors = []
    if (v.get("width"), v.get("height"), v.get("r_frame_rate")) != (1920, 1080, "30/1"):
        errors.append("unexpected video resolution or frame rate")
    if a.get("sample_rate") != "48000":
        errors.append("missing or wrong-rate audio")
    if abs(duration - plan["duration_seconds"]) > 0.7:
        errors.append("duration does not match the revised timeline")
    # Entire stream decode catches corrupt packets that spot-checks cannot.
    decoded = subprocess.run([str(FFMPEG), "-v", "error", "-xerror", "-i", str(OUTPUT),
                              "-f", "null", "-"], capture_output=True, text=True)
    if decoded.returncode:
        errors.append(f"full decode failed: {decoded.stderr[-1200:]}")
    frames = []
    for section in (1, 3, 5, 7, 8, 9, 10, 11):
        chapter = plan["chapters"][section - 1]
        next_frame = plan["chapters"][section]["frame"] if section < 11 else plan["total_frames"]
        at = (chapter["frame"] + (next_frame - chapter["frame"]) // 2) / 30
        still = ROOT / "output" / f"reedit-review-{section:02d}.png"
        subprocess.run([str(FFMPEG), "-v", "error", "-y", "-ss", str(at),
                        "-i", str(OUTPUT), "-frames:v", "1", str(still)], check=True)
        frames.append(str(still))
    report = {"output": str(OUTPUT), "type": "FFmpeg review copy, not Resolve export",
              "probe": probe, "expected_duration_seconds": plan["duration_seconds"],
              "full_stream_decode_passed": decoded.returncode == 0, "still_frames": frames,
              "automatic_checks_passed": not errors, "errors": errors,
              "manual_review_pending": ["Listen to all Venkat narration and verify spoken word/graphic sync",
                                        "Inspect screens for privacy, old terminal history and notifications",
                                        "Record missing installer/extension/interpreter/greeting-change pickups before publishing",
                                        "Import FCPXML into Resolve, check relinking, and export a Resolve master"]}
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("output", "automatic_checks_passed", "errors")}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
