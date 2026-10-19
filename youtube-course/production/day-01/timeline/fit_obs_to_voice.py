"""Time-fit genuine OBS video to the new section WAVs without inventing shots.

Outputs silent 30 fps H.264 intermediates for an editable Resolve interchange.
Each OBS source, source in-point, and speed factor is recorded in a manifest.
"""
import json
from pathlib import Path
import subprocess
import wave

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "timeline" / "reedit-media"
FFMPEG = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffmpeg.exe"))
FFPROBE = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffprobe.exe"))
FPS = 30


def main():
    voice = json.loads((ROOT / "voice/reedit-venkat/manifest.json").read_text(encoding="utf-8"))
    if voice.get("status") != "completed" or voice.get("voice_name", "").lower() != "venkat-english":
        raise RuntimeError("Voice Studio VENKAT-ENGLISH narration is required")
    shots = {c["section"]: c for c in json.loads((ROOT / "screen/obs-capture-results.json").read_text(encoding="utf-8"))["captures"]}
    DEST.mkdir(exist_ok=True)
    report = {"format": "day-01-obs-video-fit/v1", "source": "authentic OBS captures, silent retime only",
              "fps": FPS, "sections": []}
    for item in voice["sections"]:
        number = int(item["id"])
        sound = ROOT / "voice/reedit-venkat" / item["file"]
        with wave.open(str(sound), "rb") as audio:
            target_frames = round(audio.getnframes() / audio.getframerate() * FPS)
        shot = shots[number]
        # The live prompt and early hello.py run must remain visible from time 0.
        source_in = 0.0 if number in (5, 8) else 3.5
        available = shot["duration_seconds"] - source_in
        if available < 5:
            raise RuntimeError(f"Section {number:02d} lacks usable OBS media")
        target = target_frames / FPS
        factor = target / available
        if not 0.85 <= factor <= 1.30:
            raise RuntimeError(f"Unsafe visual speed factor {factor:.3f} for section {number:02d}")
        output = DEST / f"section-{number:02d}-obs-fit.mp4"
        filters = (f"trim=duration={available:.6f},setpts=(PTS-STARTPTS)*{factor:.9f},"
                   f"fps={FPS},tpad=stop_mode=clone:stop_duration=0.2,trim=end_frame={target_frames},"
                   "setpts=N/(30*TB),format=yuv420p")
        subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y", "-ss", str(source_in),
                        "-i", shot["path"], "-an", "-vf", filters, "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "19", "-r", "30", str(output)], check=True)
        probe = json.loads(subprocess.check_output([str(FFPROBE), "-v", "error", "-count_frames",
                "-show_entries", "stream=nb_read_frames", "-of", "json", str(output)], text=True))
        measured = int(probe["streams"][0]["nb_read_frames"])
        if measured != target_frames:
            raise RuntimeError(f"Section {number:02d} has {measured} frames; expected {target_frames}")
        report["sections"].append({"section": number, "original_obs": shot["path"],
                                   "source_in_seconds": source_in, "source_span_seconds": available,
                                   "visual_duration_seconds": target, "speed_factor": factor,
                                   "output": str(output), "frames": measured,
                                   "note": "Retime of real footage; missing actions were not manufactured"})
        print(f"Fitted OBS {number:02d}/11: {factor:.3f}× visual duration, {target:.2f}s", flush=True)
    (DEST / "manifest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Source provenance: {DEST / 'manifest.json'}")


if __name__ == "__main__":
    main()
