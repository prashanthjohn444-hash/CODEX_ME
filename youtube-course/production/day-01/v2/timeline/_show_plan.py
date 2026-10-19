import json
from pathlib import Path

base = Path(__file__).parent
p = json.loads((base / "edit-plan-v2.json").read_text(encoding="utf-8"))

print("TOTAL FRAMES:", p["total_frames"], "=", p["total_seconds"], "s")
print()
print("SECTION SLOTS (V1 DEMO CAPTURES / A1 NARRATION):")
for s in p["sections"]:
    origin = next((c for c in p["timeline_clips"]
                   if c["track"] == 1 and c["section"] == s["id"]), None)
    tag = "PLACEHOLDER" if origin and origin["origin"] == "placeholder" else "capture"
    print(f"  S{s['id']}  f{s['start_frame']:>5}-{s['end_frame']:>5}  {s['frames']:>4}f "
          f"({s['timeline_duration']:.3f}s)  narr={s['narration_duration']:.3f}s  "
          f"delta={s['delta_seconds']:+.4f}s  [{tag}]")
print()
print("B-ROLL PLACEMENTS (V2):")
for b in p["broll_placements"]:
    print(f"  S{b['section']}  {b['stem']:<16} cue_frame={b['record_frame']:>5}  "
          f"{b['frames']:>3}f ({b['frames']/30:.3f}s)  abs_t={b['absolute_start_seconds']:>7.3f}s")
    print(f"        sentence#{b['cue_sentence_index']}: {b['cue_sentence'][:70]}")
print()
print("MEDIA POOL (", len(p["media_pool"]), "files ):")
for m in p["media_pool"]:
    print(f"  {m['type']:<11} {m['key']:<24} {m['path']}")
print()
print("MARKERS:", [(m["frame"], m["name"]) for m in p["markers"]])
print()
print("PROBLEMS:", p["problems"] or "none")
