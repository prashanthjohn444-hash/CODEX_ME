# Day 23 — Python Virtual Environments

Source: **Day 23 — Virtual Environment**, Module 4 · Applied. Extracted text: [source](../source/day-23.txt).

Status: production brief; English narration confirmed, personal voice matching pending. No recording or performance data supplied. Plan one main lesson every two weeks within the confirmed under-four-hour weekly capacity.
Planning target: **8–15 minutes**, including live typing, demonstrations, and practice pauses. This is not a measured runtime.

## Promise and proof

After this lesson, the learner can **create, activate, inspect, and recreate a project environment**.
Opening proof: Create two environments and install Flask in only one; compare the interpreter and installed-package lists.
Misconception to resolve: Assuming the editor selected the interpreter from the activated terminal.

## Packaging

Editorial recommendation: **Python venv: Isolate Packages | Day 23** — linter 100/100.
Keep the topic/outcome early and the course-day label at the end. The recommendation uses lesson fit as well as the linter; it need not be the highest numeric score.

Top three by linter (ties preserve candidate order):

| Title | Score | Specific issues |
| --- | --- | --- |
| Python venv: Isolate Packages  /  Day 23 | 100 | No linter flags |
| Python Virtual Environments for Beginners  /  Day 23 | 98 | a mobile feed shows about "Python Virtual Environments for..." - check the subject survives |
| Learn Python Virtual Environments  /  Day 23 | 98 | a mobile feed shows about "Learn Python Virtual Environments  /  Day..." - check the subject survives |

Second editorial option: Python Virtual Environments for Beginners | Day 23
Recommended-title flags: None from the tool.
Thumbnail text: **SEPARATE TOOLBOXES**.
Thumbnail brief: dark charcoal background, one enlarged code/output contrast from this demo: Create two environments and install Flask in only one; compare the interpreter and installed-package lists. Yellow text, blue code accent; hide tiny editor chrome. Keep text to the stated three words or fewer. If a face is used, show a natural questioning expression facing the output; a faceless layout is equally workable. Check readability at small feed size.

## Hook options — five scored, top two shown

Scores are writing heuristics, not predictions of views or retention. Use the two below as reading options; keep the one that sounds natural and matches the opening shot.

| Hook | Verdict | Specificity | Address | Stakes | Curiosity | Brevity | Detected formula |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Before you copy this Python example, predict what will happen. Your Day 23 lab starts with virtual environments. | 70 (WORKABLE) | 74 | 96 | 62 | 58 | 100 | The Warning |
| I'm going to show you virtual environments in Python, with the result on screen before we explain the code. | 53 (WEAK) | 40 | 76 | 48 | 41 | 100 | The Reveal |

Top-scoring hook's intended structure: **The Warning — avoid passive copying**. It introduces the lesson's actual demonstration or asks the question the demonstration resolves. The detector's keyword label may differ.

## Script beat sheet

These are recording directions, not a word-for-word script. See the separate Day 1 pilot for a spoken draft.
1. **Hook / first ~15 seconds.** [ON SCREEN: the actual output or error from the demo.] Say one selected hook, then show evidence: Create two environments and install Flask in only one; compare the interpreter and installed-package lists.
2. **Turn / next ~30 seconds.** [ON SCREEN: editor and a compact branch of this day's mind map.] Say: 'We will create, activate, inspect, and recreate a project environment. First, predict what this example will do.'
3. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Show different package lists in two environments. Ask for a prediction before running; explain the observed result afterward.
4. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Create an environment with python -m venv .venv. Ask for a prediction before running; explain the observed result afterward.
5. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Show platform-specific activation and select the editor interpreter. Ask for a prediction before running; explain the observed result afterward.
6. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Freeze dependencies, deactivate, and explain why .venv is excluded from source control. Ask for a prediction before running; explain the observed result afterward.
7. **Payoff.** [ON SCREEN: the opening example running correctly.] Say: “Now you can create, activate, inspect, and recreate a project environment. Here is the result we started with.”
8. **Practice / single CTA.** [ON SCREEN: challenge card and matching HTML exercises.] Say: “Create .venv, install Flask, save requirements.txt, and identify the selected interpreter. Pause here and try it before opening the solution.”

## Short to capture inside this lesson

Self-contained moment: **Activation and the editor's interpreter selection are separate checks**.
Replacement opening: 'Why does your Python editor miss a package that works in your terminal?' — hook score 47/100.
First-two-second text: **SEPARATE TOOLBOXES**. Explain the contrast, show the run, end with the rule that resolves the opening question.
Record a 20–55 second self-contained take within the long lesson. Crop to the relevant code and terminal; do not squeeze the entire desktop into portrait. Loop by returning to the opening input or error on the last frame. Exact clip in/out points await the final timestamped transcript.

## Search package

Target queries (editorial hypotheses, not measured search demand):
- Python Virtual Environments for beginners — words covered in title + first two description lines.
- learn Python Virtual Environments — words covered in title + first two description lines.
- Python Virtual Environments tutorial — words covered in title + first two description lines.

Description draft — replace bracketed fields before upload:

```text
Python Virtual Environments for beginners: follow a worked example to create, activate, inspect, and recreate a project environment.
Learn Python Virtual Environments step by step in this Day 23 tutorial from Python 30 Days.

Course lab and mind maps: [ADD YOUR PUBLIC LAB LINK]
Course playlist: [ADD PLAYLIST LINK]
Day 23 example files: [ADD CODE LINK]

[INSERT VERIFIED CHAPTERS AFTER EDITING]

Practice challenge: Create .venv, install Flask, save requirements.txt, and identify the selected interpreter.
Preparation: Review the preceding course lessons and run their examples.
This lesson covers: Show different package lists in two environments; Create an environment with python -m venv .venv; Show platform-specific activation and select the editor interpreter; Freeze dependencies, deactivate, and explain why .venv is excluded from source control.
Use the matching HTML lesson for the full method reference and Level 1–3 exercises.
```

Tags: Python, Python 3, Virtual Environments, Python beginners, Python 30 Days. Tags are a small disambiguation aid.

## Chapter labels

Untimed plan; assign boundaries from the final edit, not this outline:
- Compare isolated project tools
- Create your virtual environment
- Activate and select Python
- Save the dependency list
- Recreate the project setup

Final validation: first chapter 00:00, at least three chapters, ascending boundaries, every chapter including the last at least ten seconds.

## Editing, comments, and retention

- Keep the learner's prediction and the output readable. Retain pauses that allow inspection; remove installation waits and repeated takes. Inspect 'Assuming the editor selected the interpreter from the activated terminal' closely in the final edit.
- Draft creator pin: “Day 23 challenge: Create .venv, install Flask, save requirements.txt, and identify the selected interpreter. Which step needs another example?” Replace this with a real recurring learner question when comments arrive.
- After publication, compare the opening promise with the first 30 seconds of the retention curve and inspect the largest drop against the transcript. Choose one revision from the evidence; do not assume every dip is a pacing failure.

## Full source coverage checklist

The main video prioritizes the worked example. Briefly orient viewers to the remaining source topics, and use the HTML as the reference lab; split dense sections into a follow-up rather than silently claiming exhaustive video coverage.

- [ ] Setting up virtual environments
- [ ] Why a virtual environment
- [ ] Commands
- [ ] pip install virtualenv
- [ ] Create the project folder
- [ ] virtualenv venv / python -m venv venv
- [ ] ls / dir
- [ ] Activate (macOS / Linux)
- [ ] Activate (Windows PowerShell)
- [ ] Activate (Windows Git Bash)
- [ ] pip freeze (empty project)
- [ ] pip install Flask
- [ ] pip freeze (after Flask)
- [ ] deactivate
- [ ] Add venv to .gitignore
- [ ] Command table
- [ ] Exercises
- [ ] Level 1
- [ ] Level 2
- [ ] Level 3

```text
Record next: Day 23 — Python venv: Isolate Packages | Day 23
Opening artifact: Create two environments and install Flask in only one; compare the interpreter and installed-package lists.
```

ship it, or change it?
