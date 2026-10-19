"""Render a *review* copy of the revised FCPXML edit plan, without touching v1.

The matching editable handoff is reedit-resolve-import.fcpxml. This renderer is
not a DaVinci Resolve export; it only gives a deterministic viewing copy.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "timeline" / "reedit-plan.json"
OUT = ROOT / "output" / "python-day-01-reedit-review.mp4"
FFMPEG = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffmpeg.exe"))
FFPROBE = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffprobe.exe"))


def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    fps = plan["fps"]
    assert fps == 30
    OUT.parent.mkdir(exist_ok=True)
    parts = []
    for section in range(1, 12):
        clips = [c for c in plan["clips"] if c["section"] == section]
        base = next(c for c in clips if c["kind"] == "video" and c["track"] == 1)
        sound = next(c for c in clips if c["kind"] == "audio")
        graphics = sorted((c for c in clips if c["kind"] == "video" and c["track"] == 2), key=lambda c: c["record_frame"])
        length = base["duration_frames"] / fps
        segment = OUT.parent / f"reedit-section-{section:02d}.mp4"
        cmd = [str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y",
               "-ss", str(base["source_in_frame"] / fps), "-i", base["path"],
               "-ss", str(sound["source_in_frame"] / fps), "-i", sound["path"]]
        for overlay in graphics:
            cmd += ["-ss", str(overlay["source_in_frame"] / fps), "-i", overlay["path"]]
        filters = [f"[0:v]fps=30,trim=duration={length},setpts=PTS-STARTPTS[base]"]
        previous = "base"
        for index, graphic in enumerate(graphics, 2):
            offset = (graphic["record_frame"] - base["record_frame"]) / fps
            duration = graphic["duration_frames"] / fps
            filters.append(f"[{index}:v]fps=30,trim=duration={duration},setpts=PTS-STARTPTS+{offset}/TB[g{index}]")
            output = f"v{index}"
            filters.append(f"[{previous}][g{index}]overlay=x=0:y=0:eof_action=pass:shortest=0[{output}]")
            previous = output
        cmd += ["-filter_complex", ";".join(filters), "-map", f"[{previous}]", "-map", "1:a:0",
                "-t", str(length), "-r", "30", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000",
                "-b:a", "192k", str(segment)]
        subprocess.run(cmd, check=True)
        parts.append(segment)
        print(f"Rendered section {section:02d}/11", flush=True)
    concat = OUT.parent / "reedit-concat.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y", "-f", "concat",
                    "-safe", "0", "-i", str(concat), "-c", "copy", str(OUT)], check=True)
    probe = subprocess.check_output([str(FFPROBE), "-v", "error", "-show_entries",
                                     "format=duration,size:stream=codec_type,width,height,r_frame_rate,sample_rate",
                                     "-of", "json", str(OUT)], text=True)
    print(f"Review copy (not Resolve export): {OUT}\n{probe}")


if __name__ == "__main__":
    main()
