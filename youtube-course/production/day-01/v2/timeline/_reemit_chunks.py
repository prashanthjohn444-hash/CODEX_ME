"""Re-emit the Resolve console chunks from the existing edit plan.

The fit math lives in resolve_build_v2.py; the plan in edit-plan-v2.json is
already computed and unchanged, so the chunk text can be regenerated without
re-probing every capture with ffprobe.

    python _reemit_chunks.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import resolve_build_v2 as rb  # noqa: E402

plan = json.loads((HERE / "edit-plan-v2.json").read_text(encoding="utf-8"))
written = rb.emit_chunks(plan)
for p in written:
    print(f"wrote {p.name} ({p.stat().st_size} bytes)")
