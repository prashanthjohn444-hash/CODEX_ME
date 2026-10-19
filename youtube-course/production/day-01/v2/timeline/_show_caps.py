import json
from pathlib import Path

base = Path(__file__).parent
p = json.loads((base / "edit-plan-v2.json").read_text(encoding="utf-8"))
print("V1 DEMO CAPTURES (source vs slot):")
short = []
for c in p["timeline_clips"]:
    if c["track"] == 1:
        sec = next(s for s in p["sections"] if s["id"] == c["section"])
        cap = p["captures"][c["section"]]
        placed = c["placed_frames"]
        flag = "" if placed >= sec["frames"] else "  <-- SHORTER THAN SLOT"
        if placed < sec["frames"]:
            short.append((c["section"], placed, sec["frames"]))
        print(f"  S{c['section']}  capture={cap.get('duration_seconds'):.3f}s "
              f"({int(round(cap.get('duration_seconds',0)*30))}f)  slot={sec['frames']}f "
              f"placed={placed}f  gap={sec['frames']-placed}f{flag}")
print()
print("SHORT CAPTURES:", short or "none")
print()
print("TRACK NAMES / structure:", p["tracks"])
