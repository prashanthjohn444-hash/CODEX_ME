"""Short Adam test render: one sentence -> voice/v2/test-adam.wav (48 kHz mono PCM16)."""

import json
import pathlib
import subprocess
import time
import urllib.request
import uuid
import wave

BASE = "http://127.0.0.1:3900"
HERE = pathlib.Path(__file__).resolve().parent
OUTPUTS = pathlib.Path.home() / "AppData/Roaming/OmniVoice/outputs"
FFMPEG = next((pathlib.Path.home() / "AppData/Roaming/OmniVoice/media_tools").rglob("ffmpeg.exe"))
PROFILE = "d8f312f3"
TEXT = "Why does your Python file show nothing when the shell shows 30?"


def multipart(fields, files):
    boundary = uuid.uuid4().hex
    body = b""
    for key, value in fields.items():
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n").encode()
    for key, (name, data) in files.items():
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"; filename=\"{name}\"\r\n"
                 f"Content-Type: application/octet-stream\r\n\r\n").encode() + data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return body, {"Content-Type": f"multipart/form-data; boundary={boundary}"}


def main():
    started = time.time()
    body, headers = multipart(
        {"text": TEXT, "language": "English", "profile_id": PROFILE},
        {},
    )
    request = urllib.request.Request(BASE + "/generate", body, headers)
    with urllib.request.urlopen(request, timeout=3600) as response:
        data = response.read()
        content_type = response.headers.get("Content-Type", "")
    print(f"content-type: {content_type} bytes: {len(data)} head: {data[:32]!r}")
    print(f"request took {time.time() - started:.1f}s")

    if data[:4] == b"RIFF":
        source = HERE / "test-adam-raw.wav"
    elif data[:3] == b"ID3" or data[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"):
        source = HERE / "test-adam-raw.mp3"
    elif data[4:8] == b"ftyp":
        source = HERE / "test-adam-raw.m4a"
    elif data[:1] == b"{":
        payload = json.loads(data)
        print("generate response:", json.dumps(payload, indent=2)[:2000])
        source = None
        for key in ("path", "file", "output", "audio_path", "filename", "output_path"):
            value = payload.get(key) if isinstance(payload, dict) else None
            if isinstance(value, str) and value:
                source = pathlib.Path(value) if pathlib.Path(value).is_file() else OUTPUTS / value
                break
        if source is None or not source.is_file():
            raise SystemExit(f"Could not locate rendered audio from response: {payload}")
    else:
        raise SystemExit(f"Unrecognised response body: {data[:64]!r}")
    source.write_bytes(data)

    target = HERE / "test-adam.wav"
    subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(target)], check=True)
    with wave.open(str(target), "rb") as reader:
        frames, rate, channels, width = reader.getnframes(), reader.getframerate(), reader.getnchannels(), reader.getsampwidth()
    duration = frames / rate
    result = {"source": str(source), "file": target.name, "duration_seconds": duration,
              "sample_rate_hz": rate, "channels": channels, "sample_width_bytes": width,
              "response_content_type": content_type, "response_bytes": len(data),
              "ok": duration > 1.0 and rate == 48000 and channels == 1 and width == 2}
    (HERE / "test-adam.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    try:
        source.unlink()
    except OSError:
        pass
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
