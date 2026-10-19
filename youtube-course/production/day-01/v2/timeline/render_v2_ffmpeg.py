"""Render a complete, deterministic master video of Day 1 v2 with FULL-LENGTH VS Code tutorials.

Combines:
  1. Full-length authentic VS Code tutorial recordings (matching section audio durations)
  2. B-roll overlay clips at exact speech/frame cue points
  3. Adam narration audio (48 kHz mono PCM / AAC)
Outputs:
  output/python-day-01-v2-master.mp4 (1920x1080 @ 30fps)
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\lms-work\Documents\Python\youtube-course\production\day-01")
PLAN_PATH = ROOT / "v2" / "timeline" / "edit-plan-v2.json"
OUT_DIR = ROOT / "output"
OUT_FILE = OUT_DIR / "python-day-01-v2-master.mp4"

FFMPEG = ROOT / "broll" / "node_modules" / "ffmpeg-static" / "ffmpeg.exe"
FFPROBE = ROOT / "broll" / "node_modules" / "ffprobe-static" / "bin" / "win32" / "x64" / "ffprobe.exe"


def render_section(section_data, brolls, section_idx, total_sections):
    sec_id = section_data["id"]
    slot_frames = section_data["slot_frames"]
    fps = 30.0
    slot_dur = slot_frames / fps
    sec_rec_frame = section_data["record_frame"]
    
    seg_path = OUT_DIR / f"v2-section-{sec_id}.mp4"
    
    inputs = []
    filter_complex = []
    
    # Input 0: base full-length VS Code tutorial capture
    inputs.extend(["-i", section_data["media_path"]])
    cap_idx = 0
    
    # Input audio
    audio_idx = 1
    inputs.extend(["-i", section_data["wav_path"]])
    
    # Input B-roll(s)
    broll_indices = []
    for b in brolls:
        b_idx = len(inputs) // 2
        inputs.extend(["-i", b["media_path"]])
        broll_indices.append((b_idx, b))
    
    # Base video: trim directly to exact slot duration (no freeze-frame hold!)
    filter_complex.append(f"[{cap_idx}:v]fps=30,trim=duration={slot_dur:.4f},setpts=PTS-STARTPTS[base]")
    
    # Apply B-roll overlays
    prev_v = "base"
    for b_idx, b in broll_indices:
        b_rec_frame = b["record_frame"]
        rel_frame = b_rec_frame - sec_rec_frame
        offset_sec = max(0.0, rel_frame / fps)
        dwell_sec = b["dwell_frames"] / fps
        
        b_out = f"b_{b_idx}"
        filter_complex.append(
            f"[{b_idx}:v]fps=30,trim=duration={dwell_sec:.4f},setpts=PTS-STARTPTS+{offset_sec:.4f}/TB[{b_out}]"
        )
        overlay_out = f"v_ov_{b_idx}"
        filter_complex.append(
            f"[{prev_v}][{b_out}]overlay=x=0:y=0:eof_action=pass:shortest=0[{overlay_out}]"
        )
        prev_v = overlay_out
    
    # Force exact slot duration on final video stream
    filter_complex.append(f"[{prev_v}]fps=30,trim=duration={slot_dur:.4f},setpts=PTS-STARTPTS[outv]")
    
    # Audio filter
    filter_complex.append(f"[{audio_idx}:a]atrim=duration={slot_dur:.4f},asetpts=PTS-STARTPTS[outa]")
    
    cmd = [
        str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y",
        *inputs,
        "-filter_complex", ";".join(filter_complex),
        "-map", "[outv]",
        "-map", "[outa]",
        "-t", f"{slot_dur:.4f}",
        "-r", "30",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-ar", "48000",
        "-b:a", "192k",
        str(seg_path)
    ]
    
    print(f"[{sec_id}/{total_sections:02d}] Rendering section {sec_id} ({slot_dur:.2f}s, {len(brolls)} b-roll)...", flush=True)
    subprocess.run(cmd, check=True)
    return seg_path


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        plan = json.load(f)
    
    sections = plan["sections_media"]
    all_brolls = plan["broll_placements"]
    
    seg_paths = []
    for idx, sec in enumerate(sections, 1):
        sec_id = sec["id"]
        brolls = [b for b in all_brolls if b["section"] == sec_id]
        seg_p = render_section(sec, brolls, idx, len(sections))
        seg_paths.append(seg_p)
    
    print("\nConcatenating master video...", flush=True)
    concat_list = OUT_DIR / "v2-concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in seg_paths:
            f.write(f"file '{p.resolve().as_posix()}'\n")
            
    concat_cmd = [
        str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(OUT_FILE)
    ]
    subprocess.run(concat_cmd, check=True)
    
    print(f"\n Master deliverable created: {OUT_FILE}", flush=True)
    
    # Probe result
    probe_proc = subprocess.run(
        [str(FFPROBE), "-v", "error", "-show_entries",
         "format=duration,size,bit_rate:stream=codec_type,width,height,r_frame_rate,sample_rate,channels",
         "-of", "json", str(OUT_FILE)],
        capture_output=True, text=True, check=True
    )
    probe = json.loads(probe_proc.stdout)
    fmt = probe["format"]
    streams = probe["streams"]
    v_stream = next(s for s in streams if s["codec_type"] == "video")
    a_stream = next(s for s in streams if s["codec_type"] == "audio")
    
    dur = float(fmt["duration"])
    size_mb = int(fmt["size"]) / (1024 * 1024)
    print(f"Duration: {dur:.2f}s ({dur/60:.2f} min)")
    print(f"Size: {size_mb:.2f} MB")
    print(f"Video: {v_stream['width']}x{v_stream['height']} @ {v_stream['r_frame_rate']} fps")
    print(f"Audio: {a_stream['sample_rate']} Hz, {a_stream['channels']} ch ({a_stream.get('codec_name', 'aac')})")
    print("\nRender completed successfully!")


if __name__ == "__main__":
    main()
