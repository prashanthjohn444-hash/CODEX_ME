"""Create clean V1 picture clips from real OBS takes and white-grid diagrams.

Every output is silent. The editable Resolve timeline places exactly one V1
picture and one A1 Venkat narration WAV per chapter (11 + 11 clips). OBS only
appears in chapters and windows with genuine recorded program actions.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "timeline" / "premium-media"
BASE = ROOT / "timeline" / "reedit-media"
GRAPHICS = ROOT / "broll" / "premium-white" / "renders"
FFMPEG = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffmpeg.exe"))
FFPROBE = next((Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffprobe.exe"))
ORIGINAL = json.loads((ROOT / "timeline" / "reedit-plan.json").read_text(encoding="utf-8"))
FRAMES = {c["section"]: c["duration_frames"] for c in ORIGINAL["clips"] if c["kind"] == "audio"}


def screen(n):
    return BASE / f"section-{n:02d}-obs-fit.mp4"


def graphic(name):
    return GRAPHICS / f"{name}.mp4"


def encode(section, inputs, chain, note):
    target = FRAMES[section]
    dest = DEST / f"section-{section:02d}-picture.mp4"
    cmd = [str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y"]
    for path in inputs:
        if not path.is_file():
            raise FileNotFoundError(path)
        cmd += ["-i", str(path)]
    cmd += ["-filter_complex", chain, "-map", "[out]", "-an", "-frames:v", str(target),
            "-r", "30", "-fps_mode", "cfr", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "20", "-pix_fmt", "yuv420p", str(dest)]
    if not dest.is_file():
        subprocess.run(cmd, check=True)
    stream = json.loads(subprocess.check_output([str(FFPROBE), "-v", "error", "-count_frames",
        "-show_entries", "stream=nb_read_frames,width,height,r_frame_rate", "-of", "json", str(dest)], text=True))["streams"][0]
    if (int(stream["nb_read_frames"]), stream["width"], stream["height"], stream["r_frame_rate"]) != (target, 1920, 1080, "30/1"):
        raise RuntimeError(f"Picture {section:02d} is not an exact {target}-frame 1080p30 clip: {stream}")
    print(f"Picture {section:02d}: {target} frames - {note.encode('ascii', 'replace').decode()}", flush=True)
    return {"section": section, "file": str(dest), "frames": target, "sources": [str(p) for p in inputs], "note": note}


def cut(n, sources, lengths, note):
    if sum(lengths) != FRAMES[n]:
        raise RuntimeError(f"Section {n} split does not equal its narration length")
    parts = [f"[{i}:v]fps=30,trim=end_frame={length},setpts=PTS-STARTPTS,format=yuv420p[v{i}]"
             for i, length in enumerate(lengths)]
    parts.append("".join(f"[v{i}]" for i in range(len(sources))) +
                 f"concat=n={len(sources)}:v=1:a=0,trim=end_frame={FRAMES[n]},setpts=N/(30*TB)[out]")
    return encode(n, sources, ";".join(parts), note)


def overlay(n, name, at, note):
    total = FRAMES[n]
    length = {5: 120, 9: 126, 10: 150}[n]
    if at + length > total:
        raise RuntimeError("Technical insert exceeds narration section")
    graph = (f"[0:v]fps=30,trim=end_frame={total},setpts=PTS-STARTPTS,format=yuv420p[base];"
             f"[1:v]fps=30,trim=end_frame={length},setpts=PTS-STARTPTS+{at}/(30*TB),format=yuv420p[insert];"
             f"[base][insert]overlay=x=0:y=0:eof_action=pass:shortest=0,"
             f"trim=end_frame={total},setpts=N/(30*TB)[out]")
    return encode(n, [screen(n), graphic(name)], graph, note)


def main():
    DEST.mkdir(exist_ok=True)
    manifest = {"format": "day-01-premium-pictures/v1", "fps": 30, "chapters": []}
    for n in (1, 2):
        manifest["chapters"].append({"section": n, "file": str(screen(n)), "frames": FRAMES[n],
                                     "sources": [str(screen(n))], "note": "OBS proof only"})
    manifest["chapters"].append(encode(3, [graphic("03-uses")],
        f"[0:v]fps=30,trim=end_frame={FRAMES[3]},setpts=N/(30*TB),format=yuv420p[out]",
        "White-grid technical examples, no fabricated usage footage"))
    manifest["chapters"].append(cut(4, [screen(4), graphic("04-install-reference")],
        [600, FRAMES[4] - 600], "Actual OBS version check, then labeled official installation reference"))
    manifest["chapters"].append(overlay(5, "05-prompt-map", 780,
        "Actual OBS prompts with a short terminal/shell diagram"))
    for n in (6, 7):
        manifest["chapters"].append({"section": n, "file": str(screen(n)), "frames": FRAMES[n],
                                     "sources": [str(screen(n))], "note": "OBS live Python demonstration"})
    # Section 08 is intentionally NOT the unrelated printed_expression.py hold.
    # In its center, reuse a genuine recorded hello.py run from chapter 02.
    total = FRAMES[8]
    lengths = [1140, 540, total - 1680]
    if lengths[2] != 792:
        raise RuntimeError("Section 08 lengths changed; realign this chapter manually")
    stretch = (540 / FRAMES[2])
    inputs = [graphic("08-editor-setup"), screen(2), graphic("08-file-checks")]
    chain = (f"[0:v]fps=30,trim=end_frame=1140,setpts=PTS-STARTPTS,format=yuv420p[a];"
             f"[1:v]fps=30,trim=end_frame={FRAMES[2]},setpts=(PTS-STARTPTS)*{stretch:.9f},"
             f"fps=30,tpad=stop_mode=clone:stop_duration=0.2,trim=end_frame=540,setpts=N/(30*TB),format=yuv420p[b];"
             f"[2:v]fps=30,trim=end_frame=792,setpts=PTS-STARTPTS,format=yuv420p[c];"
             f"[a][b][c]concat=n=3:v=1:a=0,trim=end_frame={total},setpts=N/(30*TB)[out]")
    manifest["chapters"].append(encode(8, inputs, chain,
        "Editor reference → genuine OBS hello.py execution → file checks; no fake installer"))
    manifest["chapters"].append(overlay(9, "09-shell-vs-file", 300,
        "Actual OBS comparison plus correctly named expression_only.py diagram"))
    manifest["chapters"].append(overlay(10, "10-types", 300,
        "Actual OBS type() calls plus four-value type diagram"))
    manifest["chapters"].append(encode(11, [graphic("11-challenge")],
        f"[0:v]fps=30,trim=end_frame={FRAMES[11]},setpts=N/(30*TB),format=yuv420p[out]",
        "Unanswered challenge on white grid; no fake course lab capture"))
    if sum(x["frames"] for x in manifest["chapters"]) != ORIGINAL["total_frames"]:
        raise RuntimeError("Premium picture timeline is not the exact narration length")
    (DEST / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Verified 11 picture chapters, {ORIGINAL['total_frames']} frames")


if __name__ == "__main__":
    main()
