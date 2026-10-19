"""Create an isolated OBS profile/scene collection; leave existing OBS work intact."""
import json
import os
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OBS = Path(os.environ["APPDATA"]) / "obs-studio" / "basic"
NAME = "Python30Days-Day01"
PROFILE = OBS / "profiles" / NAME
COLLECTION = OBS / "scenes" / f"{NAME}.json"
OUTPUT = ROOT / "captures"


def identifier():
    return str(uuid.uuid4())


def main():
    if COLLECTION.exists() or PROFILE.exists():
        raise SystemExit("Project OBS settings already exist; refusing to overwrite them.")
    PROFILE.mkdir(parents=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (PROFILE / "basic.ini").write_text(
        f"[General]\nName={NAME}\n\n"
        "[Video]\nBaseCX=1920\nBaseCY=1080\nOutputCX=1920\nOutputCY=1080\nFPSType=0\nFPSCommon=30\n\n"
        f"[SimpleOutput]\nFilePath={OUTPUT}\nRecFormat2=mkv\n"
        "RecQuality=HQ\nRecEncoder=x264\n\n"
        "[Output]\nMode=Simple\n\n"
        "[Audio]\nSampleRate=48000\nChannelSetup=Stereo\n",
        encoding="utf-8",
    )
    template = OBS / "scenes" / "Untitled.json"
    if not template.exists():
        raise FileNotFoundError("Existing OBS scene template missing; cannot safely create scene collection")
    data = json.loads(template.read_text(encoding="utf-8-sig"))
    data["name"] = NAME
    scene = next(source for source in data["sources"] if source["id"] == "scene")
    scene["name"] = "VS Code screen"
    scene["uuid"] = identifier()
    scene["canvas_uuid"] = identifier()
    display = {
        "prev_ver": data.get("prev_ver", 537001986),
        "name": "Display 1 — VS Code demonstration",
        "uuid": identifier(), "id": "monitor_capture", "versioned_id": "monitor_capture",
        "settings": {"monitor": 0, "capture_cursor": True},
        "mixers": 0, "sync": 0, "flags": 0, "volume": 1.0,
        "balance": 0.5, "enabled": True, "muted": False,
        "hotkeys": {}, "deinterlace_mode": 0,
        "deinterlace_field_order": 0, "monitoring_type": 0,
        "private_settings": {},
    }
    scene["settings"]["items"] = [{
        "name": display["name"], "source_uuid": display["uuid"],
        "visible": True, "locked": True, "id": 1,
        "pos": {"x": 0.0, "y": 0.0},
        "scale": {"x": 1.0, "y": 1.0},
        "rot": 0.0, "align": 5, "bounds_type": 0,
        "bounds_align": 0, "bounds": {"x": 0.0, "y": 0.0},
        "crop_left": 0, "crop_top": 0, "crop_right": 0, "crop_bottom": 0,
        "group_item_backup": False, "scale_filter": "disable",
        "blend_method": "default", "blend_type": "normal",
    }]
    data["sources"].append(display)
    data["scene_order"] = [{"name": scene["name"]}]
    data["current_scene"] = scene["name"]
    data["current_program_scene"] = scene["name"]
    # No unrelated desktop or microphone audio in the screen-capture footage.
    for key in ("DesktopAudioDevice1", "AuxAudioDevice1"):
        data.pop(key, None)
    COLLECTION.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Created {PROFILE} and {COLLECTION}; OBS recording path: {OUTPUT}")
    print("Before recording, open source Properties in OBS and select the primary Display. OBS writes monitor_id for this specific machine; monitor=0 alone can render black.")


if __name__ == "__main__":
    main()
