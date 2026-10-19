"""Transfer verified OBS results into the original shot manifest."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.json"
RESULTS = ROOT / "obs-capture-results.json"


def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    if results["status"] != "captured_pending_visual_review":
        raise RuntimeError("All OBS takes must finish before updating the shot manifest")
    captures = {c["section"]: c for c in results["captures"]}
    if set(captures) != set(range(1, 12)):
        raise RuntimeError("Missing numbered sections")
    for shot in data["shots"]:
        take = captures[shot["section"]]
        path = Path(take["path"])
        if not path.is_file() or path.stat().st_size == 0:
            raise FileNotFoundError(path)
        shot.update(path=str(path.relative_to(ROOT)), duration_seconds=take["duration_seconds"],
                    status="captured_pending_visual_review")
    data.update(status="captured_pending_visual_review",
                editor="VS Code (approved by user)", recorder="OBS Studio 32.2.2",
                capabilities={"python": "Recorded Python 3.13.15 on host",
                              "screen_capture": "OBS Studio, 1920x1080 at 30 fps; test frame visually inspected"},
                gaps=["Inspect every numbered take before publishing.",
                      "Section 08 editor installation web/extension views may need supplemental footage."])
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Updated eleven shot records from verified OBS assets")


if __name__ == "__main__":
    main()
