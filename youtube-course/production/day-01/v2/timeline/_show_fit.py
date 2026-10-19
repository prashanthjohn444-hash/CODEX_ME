import json
from pathlib import Path

p = json.loads((Path(__file__).parent / "edit-plan-v2.json").read_text(encoding="utf-8"))
FPS = 30
print(f"TOTAL {p['total_frames']}f = {p['total_seconds']}s   narration {p['narration_seconds']}s")
print()
print(f"{'sec':<4}{'slot':>6}{'start':>7}{'cap_f':>7}{'pct':>9}{'x':>6}{'stretch':>8}{'hold_f':>7}{'hold_s':>7}{'sum':>7}  fill")
for s in p["sections_media"]:
    st = s.get("stretched_frames", s["slot_frames"])
    hd = s.get("hold_frames", 0)
    print(f"{s['id']:<4}{s['slot_frames']:>6}{s['record_frame']:>7}{s.get('capture_frames',0):>7}"
          f"{s.get('speed_pct',100):>8.2f}%{s.get('speed_multiplier',1):>6.2f}{st:>8}{hd:>7}"
          f"{hd/FPS:>7.2f}{st+hd:>7}  {s['fill']}")
print()
print(f"{'sec':<4}{'stem':<17}{'cue_f':>7}{'cue_s':>8}{'clip_f':>7}{'dwell_f':>8}{'dwell_s':>8}{'cov':>6}  dwell?")
for b in p["broll_placements"]:
    print(f"{b['section']:<4}{b['stem']:<17}{b['record_frame']:>7}{b['absolute_start_seconds']:>8.2f}"
          f"{b['clip_frames']:>7}{b['dwell_frames']:>8}{b['dwell_seconds']:>8.2f}"
          f"{b['speech_coverage']*100:>5.0f}%  {'yes' if b['dwell_extended_for_hold'] else ''}")
print()
print("PROBLEMS:", p["problems"] or "none")
print("MISSING:", p["missing_or_incomplete_captures"] or "none")
print("media pool:", len(p["media_pool"]), "markers:", len(p["markers"]))
tot_hold = sum(s.get("hold_frames", 0) for s in p["sections_media"])
print(f"freeze-hold total: {tot_hold}f = {tot_hold/FPS:.1f}s = {tot_hold/p['total_frames']*100:.1f}% of the timeline")
sums = [s.get("stretched_frames", s["slot_frames"]) + s.get("hold_frames", 0) - s["slot_frames"] for s in p["sections_media"]]
print("slot overflow per section:", sums)
