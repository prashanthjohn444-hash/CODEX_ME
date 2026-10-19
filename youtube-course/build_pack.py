"""Build editorial briefs and run the installed skills' actual scoring functions."""
import csv
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS = ROOT.parent / ".opencode" / "skills"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hook_result(text, intended):
    parts, verdict, formula, _ = hooks.score(text)
    return dict(hook=text, properties=parts, verdict=verdict,
                band=hooks.band(verdict), detected_formula=formula, intended_formula=intended)


def cell(text):
    return str(text).replace("|", " / ").replace("\n", " ")


hooks = load("hookscore", SKILLS / "yt-script" / "hookscore.py")
titles = load("title_linter", SKILLS / "yt-package" / "title.py")
episodes = json.loads((ROOT / "episode_data.json").read_text(encoding="utf-8"))
lessons = json.loads((ROOT / "source" / "lessons.json").read_text(encoding="utf-8"))
assert len(episodes) == len(lessons) == 30
(ROOT / "episodes").mkdir(exist_ok=True)
(ROOT / "scores").mkdir(exist_ok=True)
manifest = []
all_scores = []
master = ["# Python 30 Days — video production map", "",
          "English adaptation of the supplied HTML; English narration confirmed, personal creator voice samples pending.",
          "Confirmed capacity: under four hours/week. Baseline: one main lesson every two weeks, with a three-hour weekly planning budget; about 60 weeks for 30 lessons before breaks. Shorts are optional.",
          "Thirty learning days, not a promise of thirty consecutive uploads. Each link opens a production brief, not a finished spoken script.",
          "", "| Day | Recommended title | Thumbnail | Viewer outcome | Brief |",
          "| --- | --- | --- | --- | --- |"]

for episode, lesson in zip(episodes, lessons):
    d = episode["day"]
    assert d == lesson["day"]
    subject = episode["subject"]
    topic = subject.removeprefix("Python ")
    candidates = [
        episode["title"],
        f"{subject} for Beginners | Day {d}",
        f"Learn {subject} | Day {d}",
        f"{subject}: A Worked Example | Day {d}",
        f"{subject}: Predict the Output | Day {d}",
        f"{subject}: Code Along | Day {d}",
        f"{subject}: Practice and Debug | Day {d}",
        f"{subject}: From Idea to Output | Day {d}",
        f"{subject}: Your Next Python Lab | Day {d}",
        f"{subject}: Build, Run, Explain | Day {d}",
    ]
    assert len(set(candidates)) == 10
    title_scores = sorted([titles.check(t, episode["thumb"]) for t in candidates], key=lambda t: -t["score"])
    hook_candidates = [
        (episode["question"], "The Question"),
        (f"I'm going to show you {topic.lower()} in Python, with the result on screen before we explain the code.", "The Reveal"),
        (f"By the end of this video, you can {episode['outcome']}.", "The Clock — outcome-bound, no minute guarantee"),
        (f"This is the {subject} lab: you will predict the output, run the code, and fix one mistake.", "The Receipt — record the actual working lab"),
        (f"Before you copy this Python example, predict what will happen. Your Day {d} lab starts with {topic.lower()}.", "The Warning — avoid passive copying"),
    ]
    hook_scores = sorted([hook_result(t, f) for t, f in hook_candidates], key=lambda h: -h["verdict"])
    recommended = next(t for t in title_scores if t["title"] == episode["title"])
    description = (
        f"{subject} for beginners: follow a worked example to {episode['outcome']}.\n"
        f"Learn {subject} step by step in this Day {d} tutorial from Python 30 Days.\n\n"
        "Course lab and mind maps: [ADD YOUR PUBLIC LAB LINK]\n"
        "Course playlist: [ADD PLAYLIST LINK]\n"
        f"Day {d} example files: [ADD CODE LINK]\n\n"
        "[INSERT VERIFIED CHAPTERS AFTER EDITING]\n\n"
        f"Practice challenge: {episode['challenge']}\n"
        f"Preparation: {'No programming experience needed; a computer and an editor.' if d == 1 else 'Review the preceding course lessons and run their examples.'}\n"
        f"This lesson covers: {'; '.join(episode['beats'])}.\n"
        "Use the matching HTML lesson for the full method reference and Level 1–3 exercises."
    )
    queries = [f"{subject} for beginners", f"learn {subject}", f"{subject} tutorial"]
    search_surface = (episode["title"] + " " + "\n".join(description.splitlines()[:2])).lower()
    query_checks = [{"query": q, "covered": all(w in search_surface for w in re.findall(r"\w+", q.lower()))} for q in queries]
    assert all(q["covered"] for q in query_checks)
    duration = "15–25" if d in {14, 24, 26, 27, 29} else "8–15"
    lines = [f"# Day {d:02d} — {subject}", "",
             f"Source: **{lesson['title']}**, {lesson['module']}. Extracted text: [source](../source/day-{d:02d}.txt).",
             "", "Status: production brief; English narration confirmed, personal voice matching pending. No recording or performance data supplied. Plan one main lesson every two weeks within the confirmed under-four-hour weekly capacity.",
             f"Planning target: **{duration} minutes**, including live typing, demonstrations, and practice pauses. This is not a measured runtime.",
             "", "## Promise and proof", "", f"After this lesson, the learner can **{episode['outcome']}**.",
             f"Opening proof: {episode['demo']}", f"Misconception to resolve: {episode['trap']}.",
             "", "## Packaging", "", f"Editorial recommendation: **{episode['title']}** — linter {recommended['score']}/100.",
             "Keep the topic/outcome early and the course-day label at the end. The recommendation uses lesson fit as well as the linter; it need not be the highest numeric score.",
             "", "Top three by linter (ties preserve candidate order):", "",
             "| Title | Score | Specific issues |", "| --- | --- | --- |"]
    for t in title_scores[:3]:
        lines.append(f"| {cell(t['title'])} | {t['score']} | {cell('; '.join(i[1] for i in t['issues']) or 'No linter flags')} |")
    lines += ["", "Second editorial option: " + next(t["title"] for t in title_scores if t["title"] != episode["title"]),
              f"Recommended-title flags: {'; '.join(i[1] for i in recommended['issues']) or 'None from the tool'}.",
              f"Thumbnail text: **{episode['thumb']}**.",
              f"Thumbnail brief: dark charcoal background, one enlarged code/output contrast from this demo: {episode['demo']} Yellow text, blue code accent; hide tiny editor chrome. Keep text to the stated three words or fewer. If a face is used, show a natural questioning expression facing the output; a faceless layout is equally workable. Check readability at small feed size.",
              "", "## Hook options — five scored, top two shown", "",
              "Scores are writing heuristics, not predictions of views or retention. Use the two below as reading options; keep the one that sounds natural and matches the opening shot.",
              "", "| Hook | Verdict | Specificity | Address | Stakes | Curiosity | Brevity | Detected formula |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for h in hook_scores[:2]:
        p = h["properties"]
        lines.append(f"| {cell(h['hook'])} | {h['verdict']} ({h['band']}) | {p['SPECIFICITY']} | {p['ADDRESS']} | {p['STAKES']} | {p['CURIOSITY']} | {p['BREVITY']} | {h['detected_formula']} |")
    winner = hook_scores[0]
    lines += ["", f"Top-scoring hook's intended structure: **{winner['intended_formula']}**. It introduces the lesson's actual demonstration or asks the question the demonstration resolves. The detector's keyword label may differ.",
              "", "## Script beat sheet", "",
              "These are recording directions, not a word-for-word script. See the separate Day 1 pilot for a spoken draft.",
              f"1. **Hook / first ~15 seconds.** [ON SCREEN: the actual output or error from the demo.] Say one selected hook, then show evidence: {episode['demo']}",
              f"2. **Turn / next ~30 seconds.** [ON SCREEN: editor and a compact branch of this day's mind map.] Say: 'We will {episode['outcome']}. First, predict what this example will do.'"]
    for idx, beat in enumerate(episode["beats"], 3):
        lines.append(f"{idx}. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] {beat}. Ask for a prediction before running; explain the observed result afterward.")
    lines += [f"7. **Payoff.** [ON SCREEN: the opening example running correctly.] Say: “Now you can {episode['outcome']}. Here is the result we started with.”",
              f"8. **Practice / single CTA.** [ON SCREEN: challenge card and matching HTML exercises.] Say: “{episode['challenge']} Pause here and try it before opening the solution.”",
              "", "## Short to capture inside this lesson", "",
              f"Self-contained moment: **{episode['short']}**.",
              f"Replacement opening: '{episode['question']}' — hook score {hook_result(episode['question'], 'The Question')['verdict']}/100.",
              f"First-two-second text: **{episode['thumb']}**. Explain the contrast, show the run, end with the rule that resolves the opening question.",
              "Record a 20–55 second self-contained take within the long lesson. Crop to the relevant code and terminal; do not squeeze the entire desktop into portrait. Loop by returning to the opening input or error on the last frame. Exact clip in/out points await the final timestamped transcript.",
              "", "## Search package", "", "Target queries (editorial hypotheses, not measured search demand):"]
    lines += [f"- {q['query']} — words covered in title + first two description lines." for q in query_checks]
    lines += ["", "Description draft — replace bracketed fields before upload:", "", "```text", description, "```", "",
              f"Tags: Python, Python 3, {topic}, Python beginners, Python 30 Days. Tags are a small disambiguation aid.",
              "", "## Chapter labels", "", "Untimed plan; assign boundaries from the final edit, not this outline:"]
    lines += [f"- {c}" for c in episode["chapters"]]
    lines += ["", "Final validation: first chapter 00:00, at least three chapters, ascending boundaries, every chapter including the last at least ten seconds.",
              "", "## Editing, comments, and retention", "",
              f"- Keep the learner's prediction and the output readable. Retain pauses that allow inspection; remove installation waits and repeated takes. Inspect '{episode['trap']}' closely in the final edit.",
               f"- Draft creator pin: “Day {d} challenge: {episode['challenge']} Which step needs another example?” Replace this with a real recurring learner question when comments arrive.",
              "- After publication, compare the opening promise with the first 30 seconds of the retention curve and inspect the largest drop against the transcript. Choose one revision from the evidence; do not assume every dip is a pacing failure.",
              "", "## Full source coverage checklist", "",
              "The main video prioritizes the worked example. Briefly orient viewers to the remaining source topics, and use the HTML as the reference lab; split dense sections into a follow-up rather than silently claiming exhaustive video coverage.", ""]
    lines += [f"- [ ] {item['title']}" for item in lesson["contents"]]
    lines += ["", "```text", f"Record next: Day {d} — {episode['title']}", f"Opening artifact: {episode['demo']}", "```", "", "ship it, or change it?", ""]
    path = ROOT / "episodes" / f"day-{d:02d}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    master.append(f"| {d} | {cell(episode['title'])} | {episode['thumb']} | {episode['outcome']} | [Day {d:02d}](episodes/day-{d:02d}.md) |")
    manifest.append(dict(day=d, module=lesson["module"], title=episode["title"], thumbnail=episode["thumb"], outcome=episode["outcome"], recommended_title_score=recommended["score"], top_hook_score=winner["verdict"], status="Brief ready; voice and recording pending"))
    all_scores.append(dict(day=d, titles=title_scores, hooks=hook_scores, query_checks=query_checks))

master += ["", "## Production approach", "",
           "Use each day's HTML mind map as a short orientation and recap, not a full-screen lecture. Start with code doing something observable. Demonstrate one error, repair it, and finish with one exercise.",
           "The Day 20 recording needs a short environment preview before installing packages; Day 23 remains the full environment lesson. Days 14 and 24 are dense enough to need an optional second recording.",
           "", "```text", "Next recording: Day 1 pilot → inspect the rough cut → record Days 2–3 using the revised format.", "```", "", "ship it, or change it?", ""]
(ROOT / "30-video-plan.md").write_text("\n".join(master), encoding="utf-8")
(ROOT / "scores" / "all-scores.json").write_text(json.dumps(all_scores, ensure_ascii=False, indent=2), encoding="utf-8")
with (ROOT / "production-tracker.csv").open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=manifest[0].keys())
    writer.writeheader()
    writer.writerows(manifest)
result = subprocess.run([sys.executable, str(SKILLS / "yt-viral" / "swipe.py"), str(ROOT / "research" / "public-videos.json"), "--min", "2.0", "--json"], capture_output=True, text=True, check=True)
(ROOT / "research" / "outliers.json").write_text(result.stdout, encoding="utf-8")
print("Built 30 briefs, 30-row tracker, 300 title pair checks, 150 hook panels, and 90 query coverage checks.")
print("Ran swipe.py on five sourced public videos; results saved in research/outliers.json.")
