import json
from pathlib import Path

base = Path(__file__).parent
p = json.loads((base / "edit-plan-v2.json").read_text(encoding="utf-8"))
print("B-ROLL CUE CHECK (clip window vs speech):")
for b in p["broll_placements"]:
    print(f"  S{b['section']} {b['stem']:<16} rec={b['record_frame']:>5} "
          f"win={b['window_seconds']:.3f}s speech_in_win={b['speech_seconds_in_window']:.3f}s "
          f"coverage={b['speech_coverage']*100:.0f}%")
    print(f"       sentence#{b['cue_sentence_index']}: {b['cue_sentence'][:72]}")
print("PROBLEMS:", p["problems"] or "none")
