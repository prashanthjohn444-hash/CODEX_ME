"""Render the eleven spoken sections of Day 1 with the ADAM profile on the local
VoiceStudio/OmniVoice backend, writing everything into voice/v2/.

Pipeline is the one from ../generate.py (plan -> SSE audiobook stream -> m4b ->
48 kHz mono PCM16 decode -> per-section split), plus explicit verification:
chapter count, per-section duration vs the chapter event, and a tail-energy
truncation check on the final section.
"""

import datetime
import hashlib
import json
import math
import pathlib
import re
import shutil
import struct
import subprocess
import traceback
import urllib.request
import wave

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT.parents[3] / "day-01-spoken-script.md"
BASE = "http://127.0.0.1:3900"
OUTPUTS = pathlib.Path.home() / "AppData/Roaming/OmniVoice/outputs"
FFMPEG = next((pathlib.Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffmpeg.exe"))
MANIFEST = ROOT / "manifest.json"
LOG = ROOT / "generation.log"
VOICE = "d8f312f3"                      # catalog profile id, not the demo voice
VOICE_NAME = "ADAM-ENGLISH (Consensus 90-day) (Adam)"


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


def rms_and_tail_rms(path):
    """Overall RMS and RMS of the last 0.5 s, in 16-bit full-scale units."""
    with wave.open(str(path), "rb") as reader:
        rate = reader.getframerate()
        data = reader.readframes(reader.getnframes())
    if len(data) < 4:
        return 0.0, 0.0
    samples = struct.unpack(f"<{len(data) // 2}h", data)
    overall = math.sqrt(sum(s * s for s in samples) / len(samples))
    tail = samples[-min(len(samples), int(rate * 0.5) * 1):]
    tail_rms = math.sqrt(sum(s * s for s in tail) / len(tail)) if tail else 0.0
    return round(overall, 1), round(tail_rms, 1)


def main():
    source_bytes, items = sections()
    state = {"status": "preparing", "started_utc": utc(), "source": str(SOURCE),
             "source_sha256": hashlib.sha256(source_bytes).hexdigest(), "language": "English",
             "narration_type": "synthetic; VoiceStudio/OmniVoice TTS, not human-recorded",
             "provider": "local VoiceStudio/OmniVoice backend (http://127.0.0.1:3900)",
             "voice_profile_id": VOICE, "voice_name": VOICE_NAME,
             "voice_requested_name": "Adam",
             "voice_profile_kind": "clone",
             "voice_profile_origin": "pre-existing profile in the VoiceStudio catalog "
                                     "(GET /profiles -> 'ADAM-ENGLISH (Consensus 90-day)', id d8f312f3, "
                                     "kind=clone, ref audio d8f312f3.wav); NOT the bundled demo voice",
             "provided_reference_asset": "assets/adam-reference.mp3",
             "provided_reference_used": False,
             "provided_reference_note": "user-supplied ElevenLabs 'Adam - Dominant, Firm' sample copied into "
                                        "voice/v2/assets/ for the record; the catalog already contained an "
                                        "Adam profile, which is the one rendered here.",
             "test_render": "test-adam.wav (4.24 s, 48 kHz mono PCM16, profile d8f312f3)",
             "sections": items, "section_gap_seconds": 0, "events": [], "regenerated_sections": []}
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
    log("Submitting one resumable 11-chapter render with profile " + VOICE)
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
    if whole["sample_rate_hz"] != 48000 or whole["channels"] != 1 or whole["sample_width_bytes"] != 2:
        raise RuntimeError("Unexpected audio format")
    verification = {"combined": whole, "sections": []}
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
            info = audio_info(output)
            if info["frames"] <= 0:
                raise RuntimeError(f"Section {item['id']} produced no audio")
            reported = item["render_reported_duration_ms"] / 1000.0
            overall_rms, tail_rms = rms_and_tail_rms(output)
            check = {"section": item["id"], "chapter_event_ms": item["render_reported_duration_ms"],
                     "wav_duration_seconds": round(info["duration_seconds"], 4),
                     "delta_vs_event_seconds": round(info["duration_seconds"] - reported, 4),
                     "rms": overall_rms, "last_0.5s_rms": tail_rms,
                     "has_audio": overall_rms > 100, "tail_has_audio": tail_rms > 50,
                     "truncated": False, "regenerated": False}
            if not check["has_audio"]:
                raise RuntimeError(f"Section {item['id']} is silent")
            item.update({"file": output.name, "start_seconds": cursor / 48000,
                         "end_seconds": next_frame / 48000, "audio": info, "status": "completed",
                         "verification": check})
            verification["sections"].append(check)
            cursor = next_frame
            save(state)
    # Tail truncation check: the final section must reach the very end of the
    # combined file and still carry speech energy.
    last = items[-1]
    last_check = last["verification"]
    last_check["end_seconds"] = round(whole["frames"] / 48000, 4)
    last_check["reaches_combined_end"] = abs(last["end_seconds"] - whole["frames"] / 48000) < 1e-6
    last_check["truncated"] = not (last_check["reaches_combined_end"] and last_check["tail_has_audio"])
    expected_total = sum(i["render_reported_duration_ms"] for i in items) / 1000.0
    verification["reported_total_seconds"] = round(expected_total, 4)
    verification["actual_total_seconds"] = round(whole["frames"] / 48000, 4)
    verification["total_delta_seconds"] = round(whole["frames"] / 48000 - expected_total, 4)
    verification["all_sections_present"] = len(verification["sections"]) == 11
    verification["all_non_empty"] = all(s["wav_duration_seconds"] > 0 for s in verification["sections"])
    verification["truncated_sections"] = [s["section"] for s in verification["sections"] if s["truncated"]]
    state["verification"] = verification
    state["concatenated_file"] = decoded.name
    state["concatenated_audio"] = whole
    state["chapterized_file"] = "day-01-narration.m4b"
    state["status"] = "completed"
    state["finished_utc"] = utc()
    save(state)
    log(f"Completed all 11 sections; truncated={verification['truncated_sections']}")


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
