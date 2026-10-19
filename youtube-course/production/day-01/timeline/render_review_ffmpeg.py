"""Optional quality-control MP4 if Resolve's scripting/render path is blocked.

This output is explicitly an FFmpeg review render, NOT a DaVinci Resolve
export. Keep the FCPXML/Resolve project as the editable handoff.
"""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "timeline" / "edit-plan.json"
OUTPUT = ROOT / "output" / "python-day-01-review-ffmpeg.mp4"
FFMPEG = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffmpeg.exe"))
FFPROBE = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffprobe.exe"))


def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    OUTPUT.parent.mkdir(exist_ok=True)
    sections = sorted({c["section"] for c in plan["clips"]})
    encoders = subprocess.check_output([str(FFMPEG), "-hide_banner", "-encoders"], text=True)
    video_codec = ["-c:v", "h264_nvenc", "-preset", "p4", "-cq", "21"] if "h264_nvenc" in encoders else ["-c:v", "libx264", "-preset", "fast", "-crf", "19"]
    segments = []
    for number in sections:
        group = [c for c in plan["clips"] if c["section"] == number]
        screen = next(c for c in group if c["kind"] == "video" and c["track"] == 1)
        audio = next(c for c in group if c["kind"] == "audio")
        graphics = [c for c in group if c["kind"] == "video" and c["track"] == 2]
        segment = ROOT / "output" / f"section-{number:02d}-review.mp4"
        if segment.exists():
            segments.append(segment)
            continue
        duration = screen["duration_frames"] / 30
        cmd = [str(FFMPEG), "-hide_banner", "-loglevel", "warning", "-y",
               "-ss", str(screen["source_in_frame"] / 30), "-i", screen["path"],
               "-i", audio["path"]]
        for b in graphics:
            cmd += ["-i", b["path"]]
        filters = [f"[0:v]fps=30,trim=duration={duration},setpts=PTS-STARTPTS[base]"]
        prev = "base"
        for index, graphic in enumerate(graphics, 2):
            offset = (graphic["record_frame"] - screen["record_frame"]) / 30
            filters.append(f"[{index}:v]fps=30,trim=duration={graphic['duration_frames']/30},setpts=PTS-STARTPTS+{offset}/TB[graphic{index}]")
            out = f"combined{index}"
            filters.append(f"[{prev}][graphic{index}]overlay=x=0:y=0:eof_action=pass:shortest=0[{out}]")
            prev = out
        cmd += ["-filter_complex", ";".join(filters), "-map", f"[{prev}]", "-map", "1:a:0",
                "-t", str(duration), "-r", "30", *video_codec,
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-b:a", "192k", str(segment)]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            if video_codec[1] != "h264_nvenc":
                raise
            # A listed GPU encoder may not be accessible on a remote desktop.
            cmd[cmd.index("-c:v")+1:cmd.index("-pix_fmt")] = ["libx264", "-preset", "fast", "-crf", "19"]
            subprocess.run(cmd, check=True)
        segments.append(segment)
    concat = ROOT / "output" / "review-concat.txt"
    concat.write_text("".join(f"file '{s.as_posix()}'\n" for s in segments), encoding="utf-8")
    subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "warning", "-y", "-f", "concat",
                    "-safe", "0", "-i", str(concat), "-c", "copy", str(OUTPUT)], check=True)
    result = subprocess.check_output([str(FFPROBE), "-v", "error", "-show_entries", "format=duration,size",
                                      "-of", "json", str(OUTPUT)], text=True)
    print(f"FFmpeg review render only: {OUTPUT}\n{result}")


if __name__ == "__main__":
    main()
