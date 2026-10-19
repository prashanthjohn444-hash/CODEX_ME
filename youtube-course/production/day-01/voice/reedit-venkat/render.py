"""Non-destructive 11-chapter Voice Studio render for the VENKAT-ENGLISH profile."""

import datetime
import hashlib
import json
import pathlib
import shutil
import subprocess
import urllib.request
import wave

ROOT = pathlib.Path(__file__).resolve().parent
VOICE_ROOT = ROOT.parent
SOURCE = ROOT.parents[3] / "day-01-spoken-script.md"
ORIGINAL = VOICE_ROOT / "manifest.json"
BASE = "http://127.0.0.1:3900"
VOICE = "73ef31d5"
OUTPUTS = pathlib.Path.home() / "AppData/Roaming/OmniVoice/outputs"
FFMPEG = next((pathlib.Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffmpeg.exe"))


def api(path, payload):
    request = urllib.request.Request(BASE + path, json.dumps(payload).encode("utf-8"),
                                     {"Content-Type": "application/json"})
    return urllib.request.urlopen(request, timeout=21600)


def info(path):
    with wave.open(str(path), "rb") as reader:
        frames = reader.getnframes()
        return {"sample_rate_hz": reader.getframerate(), "channels": reader.getnchannels(),
                "sample_width_bytes": reader.getsampwidth(), "frames": frames,
                "duration_seconds": frames / reader.getframerate()}


def save(state):
    (ROOT / "manifest.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    # Never replace even a partial previous run; inspect it before retrying.
    if any((ROOT / name).exists() for name in ["manifest.json", "day-01-narration.wav", "day-01-narration.m4b"]):
        raise FileExistsError("Existing reedit outputs; refusing to overwrite")
    original = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest != original["source_sha256"]:
        raise ValueError("Spoken script changed from the original narration source")
    items = [{"id": s["id"], "title": s["title"], "text": s["text"]} for s in original["sections"]]
    script = "\n\n".join(f"# {s['id']} — {s['title']}\n\n{s['text']}" for s in items)
    payload = {"text": script, "default_voice": VOICE, "language": "English", "format": "m4b",
               "paragraph_gap_ms": 350, "trim_edges": True}
    with urllib.request.urlopen(BASE + "/profiles", timeout=15) as response:
        profiles = json.load(response)
    if not any(p["id"] == VOICE and p["name"] == "VENKAT-ENGLISH" and p["language"] == "English" for p in profiles):
        raise ValueError("VENKAT-ENGLISH profile not present")
    with api("/audiobook/plan", {"text": script, "default_voice": VOICE}) as response:
        plan = json.load(response)
    if plan["chapter_count"] != 11 or any(span["voice_id"] != VOICE for c in plan["chapters"] for span in c["spans"]):
        raise ValueError("Voice or chapter mismatch in plan")
    state = {"status": "rendering", "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "source": str(SOURCE), "source_sha256": digest, "provider": "local VoiceStudio/OmniVoice",
             "voice_profile_id": VOICE, "voice_name": "VENKAT-ENGLISH", "narration_type": "synthetic clone; not a human-recorded lesson",
             "request_settings": {k: v for k, v in payload.items() if k != "text"},
             "section_gap_seconds": 0, "plan": plan, "sections": items, "events": []}
    save(state)
    with api("/audiobook", payload) as response:
        for raw in response:
            line = raw.decode("utf-8").strip()
            if line.startswith("data:"):
                event = json.loads(line[5:].strip())
                state["events"].append(event)
                if event.get("job_id"):
                    state["job_id"] = event["job_id"]
                if event.get("type") == "chapter":
                    items[event["index"]]["render_reported_duration_ms"] = event["duration_ms"]
                if event.get("type") == "done":
                    state["result"] = event
                save(state)
                print(event["type"], event.get("index", ""), event.get("duration_ms", ""), flush=True)
    if not state.get("result") or state["result"].get("failed_chapters") or len([x for x in items if "render_reported_duration_ms" in x]) != 11:
        state["status"] = "failed"
        save(state)
        raise RuntimeError("Incomplete render; see manifest events")
    voices = state["result"].get("summary", {}).get("voices", [])
    if not any(v.get("id") == VOICE for v in voices):
        raise RuntimeError(f"Rendered voice does not match requested profile: {voices}")
    m4b = ROOT / "day-01-narration.m4b"
    shutil.copyfile(OUTPUTS / state["result"]["output"], m4b)
    wav = ROOT / "day-01-narration.wav"
    subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-n", "-i", str(m4b),
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(wav)], check=True)
    whole = info(wav)
    if whole["sample_rate_hz"] != 48000 or whole["channels"] != 1:
        raise RuntimeError("Unexpected decoded format")
    cursor = 0
    with wave.open(str(wav), "rb") as reader:
        for index, item in enumerate(items):
            end = round(sum(s["render_reported_duration_ms"] for s in items[:index + 1]) * 48)
            if index == len(items) - 1:
                end = whole["frames"]
            end = min(end, whole["frames"])
            if end <= cursor:
                raise RuntimeError("Empty or misaligned chapter")
            filename = f"section-{item['id']}.wav"
            with (ROOT / filename).open("xb") as output:
                with wave.open(output, "wb") as writer:
                    writer.setnchannels(1)
                    writer.setsampwidth(2)
                    writer.setframerate(48000)
                    writer.writeframes(reader.readframes(end - cursor))
            item.update({"file": filename, "start_seconds": cursor / 48000,
                         "end_seconds": end / 48000, "audio": info(ROOT / filename), "status": "completed"})
            cursor = end
            save(state)
    state.update({"status": "completed", "concatenated_file": wav.name, "concatenated_audio": whole,
                  "chapterized_file": m4b.name, "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()})
    save(state)
    print("complete", whole["duration_seconds"], flush=True)


if __name__ == "__main__":
    main()
