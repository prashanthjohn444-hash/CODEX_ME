"""Render the eleven spoken sections of Day 1 using the local VoiceStudio API.

Run once while the backend listens on 127.0.0.1:3900. Progress is written to
manifest.json and generation.log; rerun only if no active job is running.
"""

import datetime
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import traceback
import urllib.request
import wave

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT.parents[2] / "day-01-spoken-script.md"
BASE = "http://127.0.0.1:3900"
OUTPUTS = pathlib.Path.home() / "AppData/Roaming/OmniVoice/outputs"
FFMPEG = next((pathlib.Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffmpeg.exe"))
MANIFEST = ROOT / "manifest.json"
LOG = ROOT / "generation.log"
VOICE = "demo0001"


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def log(value):
    with LOG.open("a", encoding="utf-8") as out:
        out.write(f"{utc()} {value}\n")


def save(manifest):
    temporary = MANIFEST.with_suffix(".tmp")
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(MANIFEST)


def sections():
    source_bytes = SOURCE.read_bytes()
    source = source_bytes.decode("utf-8")
    matches = list(re.finditer(r"(?m)^## (\d+)\. (.+)$", source))
    if len(matches) != 11:
        raise ValueError(f"Expected 11 numbered sections, found {len(matches)}")
    result = []
    for i, match in enumerate(matches):
        body = source[match.end():matches[i + 1].start() if i + 1 < len(matches) else source.index("## Recording notes")]
        paragraphs = [line[2:].strip() for line in body.splitlines() if line.startswith("> ")]
        if not paragraphs:
            raise ValueError(f"Section {i+1} contains no spoken text")
        result.append({"id": f"{i+1:02d}", "title": match.group(2), "text": "\n\n".join(paragraphs), "status": "pending"})
    return source_bytes, result


def post(path, body):
    request = urllib.request.Request(BASE + path, json.dumps(body).encode("utf-8"), {"Content-Type": "application/json"})
    return urllib.request.urlopen(request, timeout=21600)


def audio_info(path):
    with wave.open(str(path), "rb") as reader:
        frames = reader.getnframes()
        return {"sample_rate_hz": reader.getframerate(), "channels": reader.getnchannels(),
                "sample_width_bytes": reader.getsampwidth(), "frames": frames,
                "duration_seconds": frames / reader.getframerate()}


def main():
    source_bytes, items = sections()
    state = {"status": "preparing", "started_utc": utc(), "source": str(SOURCE),
             "source_sha256": hashlib.sha256(source_bytes).hexdigest(), "language": "English",
             "narration_type": "synthetic draft; not human-recorded",
             "provider": "local VoiceStudio/OmniVoice", "voice_profile_id": VOICE,
             "voice_name": "VoiceStudio Demo Voice (bundled English demo)",
             "sections": items, "section_gap_seconds": 0, "events": []}
    save(state)
    script = "\n\n".join(f"# {item['id']} — {item['title']}\n\n{item['text']}" for item in items)
    payload = {"text": script, "default_voice": VOICE, "language": "English", "format": "m4b",
               "paragraph_gap_ms": 350, "trim_edges": True}
    state["request_settings"] = {key: value for key, value in payload.items() if key != "text"}
    with post("/audiobook/plan", {"text": script, "default_voice": VOICE}) as response:
        plan = json.load(response)
    state["plan"] = plan
    if plan.get("chapter_count") != 11:
        raise ValueError(f"Plan did not preserve 11 chapters: {plan.get('chapter_count')}")
    state["status"] = "rendering"
    save(state)
    log("Submitting one resumable 11-chapter render")
    with post("/audiobook", payload) as response:
        for raw in response:
            line = raw.decode("utf-8").strip()
            if not line.startswith("data:"):
                continue
            event = json.loads(line[5:].strip())
            state["events"].append(event)
            log(json.dumps(event, ensure_ascii=False))
            if event.get("job_id"):
                state["job_id"] = event["job_id"]
            if event.get("type") == "chapter":
                item = items[event["index"]]
                item["status"] = "rendered"
                item["render_reported_duration_ms"] = event["duration_ms"]
            elif event.get("type") == "chapter_error":
                item = items[event["index"]]
                item["status"] = "failed"
                item["error"] = event.get("reason", event.get("error"))
            elif event.get("type") == "done":
                state["result"] = event
            elif event.get("type") in ("error", "stopped"):
                state["status"] = "failed"
                state["error_event"] = event
            save(state)
    if "result" not in state or any(item["status"] != "rendered" for item in items):
        raise RuntimeError("Incomplete narration render; inspect generation.log and manifest.json")
    source_audio = OUTPUTS / state["result"]["output"]
    if not source_audio.is_file():
        raise FileNotFoundError(source_audio)
    shutil.copyfile(source_audio, ROOT / "day-01-narration.m4b")
    decoded = ROOT / "day-01-narration.wav"
    subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y", "-i", str(source_audio),
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(decoded)], check=True)
    whole = audio_info(decoded)
    if whole["sample_rate_hz"] != 48000 or whole["channels"] != 1:
        raise RuntimeError("Unexpected audio format")
    with wave.open(str(decoded), "rb") as reader:
        cursor = 0
        for index, item in enumerate(items):
            # Chapter event durations are millisecond-rounded; the final section
            # takes all remaining decoded frames to avoid trailing sample loss.
            next_frame = round(sum(entry["render_reported_duration_ms"] for entry in items[:index+1]) * 48)
            next_frame = whole["frames"] if index == len(items) - 1 else min(next_frame, whole["frames"])
            count = next_frame - cursor
            if count <= 0:
                raise RuntimeError(f"Empty section {item['id']}")
            output = ROOT / f"section-{item['id']}.wav"
            with wave.open(str(output), "wb") as writer:
                writer.setnchannels(1)
                writer.setsampwidth(2)
                writer.setframerate(48000)
                writer.writeframes(reader.readframes(count))
            item.update({"file": output.name, "start_seconds": cursor / 48000,
                         "end_seconds": next_frame / 48000, "audio": audio_info(output), "status": "completed"})
            cursor = next_frame
            save(state)
    state["concatenated_file"] = decoded.name
    state["concatenated_audio"] = whole
    state["chapterized_file"] = "day-01-narration.m4b"
    state["status"] = "completed"
    state["finished_utc"] = utc()
    save(state)
    log("Completed all 11 sections")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log(traceback.format_exc())
        if MANIFEST.exists():
            state = json.loads(MANIFEST.read_text(encoding="utf-8"))
            state["status"] = "failed"
            state["error"] = traceback.format_exc()
            state["finished_utc"] = utc()
            save(state)
        raise
