"""Rebuild the bounded Day 1 editorial plan; no media generation."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
sources = ["youtube-course/day-01-spoken-script.md", "youtube-course/episodes/day-01.md", "youtube-course/source/day-01.txt", "youtube-course/source/lessons.json"]
hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sources}
scenes = [
    ("03-interpreter", "03", "You write instructions, and a Python interpreter executes them.", "Live diagram", ["Your instructions", "Python interpreter", "Result"], "interpreter", 6, "Make the relationship between code, interpreter and result visible."),
    ("03-uses", "03", "People use Python for automation, data analysis, web applications, and AI tools.", "Fan-out cascade", ["One language, many uses", "Automation", "Data", "Web", "AI tools"], "named destination", 7, "Orient beginners without adding a career or popularity claim."),
    ("05-prompts", "05", "The terminal starts programs. The Python shell accepts Python code.", "Compare cards", ["Terminal", "Starts programs", "Python shell", "Accepts Python code", ">>>"], "Python shell", 7, "Reinforce the prompt distinction after genuine shell footage."),
    ("09-display", "09", "Use print when your script needs to show the result.", "Compare cards", ["Shell", "Displays expression results", "Saved script", "Use print to display"], "print", 6, "Summarize the demonstrated shell/file difference without replacing execution footage."),
    ("11-practice", "11", "Pause here and try it yourself before opening the lab solution.", "Resource list", ["Your first Python file", "Print your name", "Print 10 + 20", "Inspect three types", "Change, save, run"], "Pause", 8, "Keep the practice request visible while the learner pauses; no solution shown."),
]
plan = {
    "day": 1, "status": "awaiting_verified_audio", "source_hashes": hashes,
    "timing_policy": "Section IDs are stable. No absolute or section-local cue offsets are asserted until verified audio and spoken-word timing are available. Durations below are editorial targets only.",
    "design": {"skill": ".agents/skills/dark-olive-broll/SKILL.md", "background": "#161911", "edge": "#0f0f0c", "accent": "#789858", "text": "#f1efe6", "safe_margin_percent": 6, "dimensions": [1920,1080], "fps": 30, "color_space": "Rec.709", "renderer": "HyperFrames", "audio": "silent graphics; verified narration remains in assembly"},
    "scenes": [{"id": i, "section_id": s, "spoken_cue": cue, "scene_type": kind, "on_screen_text": text, "accent_target": accent, "target_duration_seconds": dur, "learner_purpose": purpose, "section_local_start_seconds": None, "day_start_seconds": None, "reveals": "Align labels to their exact spoken terms after audio verification", "final_hold_seconds": 1.5, "replaces_code_demo": False, "source_caption": "SOURCE · Python 30 Days · Day 1 lesson"} for i,s,cue,kind,text,accent,dur,purpose in scenes],
    "not_graphics": ["Opening proof and repair remain genuine screen footage", "Installation and version checks remain genuine screen footage", "Arithmetic, syntax error, saved-file runs and type outputs remain genuine screen footage"],
}
(OUT / "cue-plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
manifest = {"day": 1, "status": "in_progress", "phase": "editorial_preflight", "cue_plan": "cue-plan.json", "source_hashes": hashes, "verified_outputs": [], "reused_assets": [], "usage": {"status": "unknown", "reason": "usage_request_failed"}, "workflow_freshness": "Installed general-video present; GitHub unreachable, freshness unknown", "qa": {"renders_created": False, "visual_verification": False, "audio_timing_verification": False}, "blockers": ["Verified audio and spoken cue timings pending"], "resume": "Receive audio/manifest.json from audio specialist; align cues, create editable HyperFrames scenes, check, preview and render under motion-graphics only. Preserve genuine code demonstrations."}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
