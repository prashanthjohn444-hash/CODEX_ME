"""Measure the Day 1 narration and score the five planned Shorts openings."""
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HOOKS_PATH = ROOT.parent / ".opencode" / "skills" / "yt-script" / "hookscore.py"
PILOT_PATH = ROOT / "day-01-spoken-script.md"
WORKFLOW_PATH = ROOT / "production-workflow.md"
SCORES_DIR = ROOT / "scores"


def load_hookscore():
    """Import the installed yt-script scorer rather than copying its logic."""
    spec = importlib.util.spec_from_file_location("hookscore", HOOKS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load installed hook scorer: {HOOKS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def narration_text(markdown):
    """Return only Markdown blockquote narration, excluding directions and code."""
    narration = []
    in_fence = False
    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        stripped = line.lstrip()
        if not in_fence and stripped.startswith(">"):
            narration.append(stripped[1:].lstrip())
    return "\n".join(narration)


def word_count(text):
    return len(re.findall(r"\b[\w]+(?:['’][\w]+)?\b", text, flags=re.UNICODE))


def short_openings(markdown):
    """Read planned source sections and replacement openings from the Shorts table."""
    openings = []
    in_section = False
    for line in markdown.splitlines():
        if line.startswith("## 3. Five pilot Shorts candidates"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section:
            continue
        match = re.match(r"^\|\s*([1-5])\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if match:
            openings.append({
                "rank": int(match.group(1)),
                "source_section": match.group(2).strip(),
                "hook": match.group(3).strip(),
            })
    assert len(openings) == 5, f"Expected five Shorts openings, found {len(openings)}"
    return openings


def main():
    hookscore = load_hookscore()
    pilot = PILOT_PATH.read_text(encoding="utf-8")
    narration = narration_text(pilot)
    words = word_count(narration)
    estimated_seconds = round(words / 150 * 60)
    pilot_metrics = {
        "source": PILOT_PATH.name,
        "counted_content": "Markdown blockquoted narration only",
        "narration_word_count": words,
        "estimate_wpm": 150,
        "estimated_narration_seconds": estimated_seconds,
        "estimated_narration_minutes": round(words / 150, 2),
        "caveat": "Narration estimate only; it excludes demonstrations, typing, and learner pauses, so it is not the expected edited runtime.",
        "excludes": ["headings", "code blocks", "on-screen directions", "typing time", "demonstration time", "learner pauses"],
    }

    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    short_scores = []
    for item in short_openings(workflow):
        properties, verdict, formula, matched = hookscore.score(item["hook"])
        short_scores.append({
            **item,
            "moment_status": "planned from the written draft",
            "clip_boundaries": None,
            "boundary_status": "pending an actual timestamped recording transcript",
            "properties": properties,
            "verdict": verdict,
            "band": hookscore.band(verdict),
            "formula": formula,
            "matched_patterns": matched,
        })

    SCORES_DIR.mkdir(exist_ok=True)
    (SCORES_DIR / "pilot-metrics.json").write_text(
        json.dumps(pilot_metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (SCORES_DIR / "short-hook-scores.json").write_text(
        json.dumps(short_scores, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Counted {words} blockquoted narration words ({words / 150:.2f} minutes at 150 wpm).")
    print("Scored five workflow Shorts openings with the installed hookscore.py functions.")


if __name__ == "__main__":
    main()
