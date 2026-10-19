# Day 12 — Python Modules

Source: **Day 12 — Modules**, Module 2 · Logic and Reuse. Extracted text: [source](../source/day-12.txt).

Status: production brief; English narration confirmed, personal voice matching pending. No recording or performance data supplied. Plan one main lesson every two weeks within the confirmed under-four-hour weekly capacity.
Planning target: **8–15 minutes**, including live typing, demonstrations, and practice pauses. This is not a measured runtime.

## Promise and proof

After this lesson, the learner can **reuse a function from another Python file**.
Opening proof: Move a helper into helpers.py and import it from main.py; compare a local module with math and statistics.
Misconception to resolve: Naming a local file random.py and shadowing the standard library.

## Packaging

Editorial recommendation: **Python Modules: Import Your Code | Day 12** — linter 98/100.
Keep the topic/outcome early and the course-day label at the end. The recommendation uses lesson fit as well as the linter; it need not be the highest numeric score.

Top three by linter (ties preserve candidate order):

| Title | Score | Specific issues |
| --- | --- | --- |
| Python Modules for Beginners  /  Day 12 | 100 | No linter flags |
| Learn Python Modules  /  Day 12 | 100 | No linter flags |
| Python Modules: Code Along  /  Day 12 | 100 | No linter flags |

Second editorial option: Python Modules for Beginners | Day 12
Recommended-title flags: a mobile feed shows about "Python Modules: Import Your Code | Day..." - check the subject survives.
Thumbnail text: **TWO FILES**.
Thumbnail brief: dark charcoal background, one enlarged code/output contrast from this demo: Move a helper into helpers.py and import it from main.py; compare a local module with math and statistics. Yellow text, blue code accent; hide tiny editor chrome. Keep text to the stated three words or fewer. If a face is used, show a natural questioning expression facing the output; a faceless layout is equally workable. Check readability at small feed size.

## Hook options — five scored, top two shown

Scores are writing heuristics, not predictions of views or retention. Use the two below as reading options; keep the one that sounds natural and matches the opening shot.

| Hook | Verdict | Specificity | Address | Stakes | Curiosity | Brevity | Detected formula |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Before you copy this Python example, predict what will happen. Your Day 12 lab starts with modules. | 70 (WORKABLE) | 74 | 96 | 62 | 58 | 100 | The Warning |
| I'm going to show you modules in Python, with the result on screen before we explain the code. | 53 (WEAK) | 40 | 76 | 48 | 41 | 100 | The Reveal |

Top-scoring hook's intended structure: **The Warning — avoid passive copying**. It introduces the lesson's actual demonstration or asks the question the demonstration resolves. The detector's keyword label may differ.

## Script beat sheet

These are recording directions, not a word-for-word script. See the separate Day 1 pilot for a spoken draft.
1. **Hook / first ~15 seconds.** [ON SCREEN: the actual output or error from the demo.] Say one selected hook, then show evidence: Move a helper into helpers.py and import it from main.py; compare a local module with math and statistics.
2. **Turn / next ~30 seconds.** [ON SCREEN: editor and a compact branch of this day's mind map.] Say: 'We will reuse a function from another Python file. First, predict what this example will do.'
3. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Show one function reused from another file. Ask for a prediction before running; explain the observed result afterward.
4. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Create a module and use import and from imports. Ask for a prediction before running; explain the observed result afterward.
5. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Use aliases and inspect where an import came from. Ask for a prediction before running; explain the observed result afterward.
6. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Tour os, sys, statistics, math, string, and random with one focused example each. Ask for a prediction before running; explain the observed result afterward.
7. **Payoff.** [ON SCREEN: the opening example running correctly.] Say: “Now you can reuse a function from another Python file. Here is the result we started with.”
8. **Practice / single CTA.** [ON SCREEN: challenge card and matching HTML exercises.] Say: “Create a helpers module and use math.sqrt() and statistics.mean() from a separate script. Pause here and try it before opening the solution.”

## Short to capture inside this lesson

Self-contained moment: **Your filename can hide a Python standard-library module**.
Replacement opening: 'Why does your Python import load the wrong file?' — hook score 44/100.
First-two-second text: **TWO FILES**. Explain the contrast, show the run, end with the rule that resolves the opening question.
Record a 20–55 second self-contained take within the long lesson. Crop to the relevant code and terminal; do not squeeze the entire desktop into portrait. Loop by returning to the opening input or error on the last frame. Exact clip in/out points await the final timestamped transcript.

## Search package

Target queries (editorial hypotheses, not measured search demand):
- Python Modules for beginners — words covered in title + first two description lines.
- learn Python Modules — words covered in title + first two description lines.
- Python Modules tutorial — words covered in title + first two description lines.

Description draft — replace bracketed fields before upload:

```text
Python Modules for beginners: follow a worked example to reuse a function from another Python file.
Learn Python Modules step by step in this Day 12 tutorial from Python 30 Days.

Course lab and mind maps: [ADD YOUR PUBLIC LAB LINK]
Course playlist: [ADD PLAYLIST LINK]
Day 12 example files: [ADD CODE LINK]

[INSERT VERIFIED CHAPTERS AFTER EDITING]

Practice challenge: Create a helpers module and use math.sqrt() and statistics.mean() from a separate script.
Preparation: Review the preceding course lessons and run their examples.
This lesson covers: Show one function reused from another file; Create a module and use import and from imports; Use aliases and inspect where an import came from; Tour os, sys, statistics, math, string, and random with one focused example each.
Use the matching HTML lesson for the full method reference and Level 1–3 exercises.
```

Tags: Python, Python 3, Modules, Python beginners, Python 30 Days. Tags are a small disambiguation aid.

## Chapter labels

Untimed plan; assign boundaries from the final edit, not this outline:
- Reuse code across files
- Create your own module
- Choose an import style
- Explore the standard library
- Try the helper challenge

Final validation: first chapter 00:00, at least three chapters, ascending boundaries, every chapter including the last at least ten seconds.

## Editing, comments, and retention

- Keep the learner's prediction and the output readable. Retain pauses that allow inspection; remove installation waits and repeated takes. Inspect 'Naming a local file random.py and shadowing the standard library' closely in the final edit.
- Draft creator pin: “Day 12 challenge: Create a helpers module and use math.sqrt() and statistics.mean() from a separate script. Which step needs another example?” Replace this with a real recurring learner question when comments arrive.
- After publication, compare the opening promise with the first 30 seconds of the retention curve and inspect the largest drop against the transcript. Choose one revision from the evidence; do not assume every dip is a pacing failure.

## Full source coverage checklist

The main video prioritizes the worked example. Briefly orient viewers to the remaining source topics, and use the HTML as the reference lab; split dense sections into a follow-up rather than silently claiming exhaustive video coverage.

- [ ] Modules
- [ ] What is a Module
- [ ] Creating a Module
- [ ] Importing a Module
- [ ] Import Functions from a Module
- [ ] Import Functions from a Module and Renaming
- [ ] Import Built-in Modules
- [ ] OS Module
- [ ] os.mkdir()
- [ ] os.chdir()
- [ ] os.getcwd()
- [ ] os.rmdir()
- [ ] Sys Module
- [ ] sys.argv
- [ ] sys.exit()
- [ ] sys.maxsize
- [ ] sys.path
- [ ] sys.version
- [ ] Statistics Module
- [ ] mean()
- [ ] median()
- [ ] mode()
- [ ] stdev()
- [ ] Math Module
- [ ] math.pi
- [ ] math.sqrt()
- [ ] math.pow()
- [ ] math.floor()
- [ ] math.ceil()
- [ ] math.log10()
- [ ] Importing from math
- [ ] String Module
- [ ] string.ascii_letters
- [ ] string.digits
- [ ] string.punctuation
- [ ] Random Module
- [ ] random()
- [ ] randint()
- [ ] Exercises
- [ ] Level 1
- [ ] Level 2
- [ ] Level 3

```text
Record next: Day 12 — Python Modules: Import Your Code | Day 12
Opening artifact: Move a helper into helpers.py and import it from main.py; compare a local module with math and statistics.
```

ship it, or change it?
