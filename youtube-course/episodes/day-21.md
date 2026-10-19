# Day 21 — Python Classes

Source: **Day 21 — Classes and Objects**, Module 3 · Intermediate. Extracted text: [source](../source/day-21.txt).

Status: production brief; English narration confirmed, personal voice matching pending. No recording or performance data supplied. Plan one main lesson every two weeks within the confirmed under-four-hour weekly capacity.
Planning target: **8–15 minutes**, including live typing, demonstrations, and practice pauses. This is not a measured runtime.

## Promise and proof

After this lesson, the learner can **model learners as objects with separate instance state**.
Opening proof: Create two Student objects, update one score with a method, and show that the other score stays unchanged.
Misconception to resolve: Accidentally sharing mutable class-level state between instances.

## Packaging

Editorial recommendation: **Python Classes and Objects | Day 21** — linter 100/100.
Keep the topic/outcome early and the course-day label at the end. The recommendation uses lesson fit as well as the linter; it need not be the highest numeric score.

Top three by linter (ties preserve candidate order):

| Title | Score | Specific issues |
| --- | --- | --- |
| Python Classes and Objects  /  Day 21 | 100 | No linter flags |
| Python Classes for Beginners  /  Day 21 | 100 | No linter flags |
| Learn Python Classes  /  Day 21 | 100 | No linter flags |

Second editorial option: Python Classes for Beginners | Day 21
Recommended-title flags: None from the tool.
Thumbnail text: **DATA + BEHAVIOR**.
Thumbnail brief: dark charcoal background, one enlarged code/output contrast from this demo: Create two Student objects, update one score with a method, and show that the other score stays unchanged. Yellow text, blue code accent; hide tiny editor chrome. Keep text to the stated three words or fewer. If a face is used, show a natural questioning expression facing the output; a faceless layout is equally workable. Check readability at small feed size.

## Hook options — five scored, top two shown

Scores are writing heuristics, not predictions of views or retention. Use the two below as reading options; keep the one that sounds natural and matches the opening shot.

| Hook | Verdict | Specificity | Address | Stakes | Curiosity | Brevity | Detected formula |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Before you copy this Python example, predict what will happen. Your Day 21 lab starts with classes. | 70 (WORKABLE) | 74 | 96 | 62 | 58 | 100 | The Warning |
| I'm going to show you classes in Python, with the result on screen before we explain the code. | 53 (WEAK) | 40 | 76 | 48 | 41 | 100 | The Reveal |

Top-scoring hook's intended structure: **The Warning — avoid passive copying**. It introduces the lesson's actual demonstration or asks the question the demonstration resolves. The detector's keyword label may differ.

## Script beat sheet

These are recording directions, not a word-for-word script. See the separate Day 1 pilot for a spoken draft.
1. **Hook / first ~15 seconds.** [ON SCREEN: the actual output or error from the demo.] Say one selected hook, then show evidence: Create two Student objects, update one score with a method, and show that the other score stays unchanged.
2. **Turn / next ~30 seconds.** [ON SCREEN: editor and a compact branch of this day's mind map.] Say: 'We will model learners as objects with separate instance state. First, predict what this example will do.'
3. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Show two objects with distinct values. Ask for a prediction before running; explain the observed result afterward.
4. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Define a class, __init__(), and instance attributes. Ask for a prediction before running; explain the observed result afterward.
5. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Write methods and distinguish instance from class attributes. Ask for a prediction before running; explain the observed result afterward.
6. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Demonstrate inheritance and method overriding with one small extension. Ask for a prediction before running; explain the observed result afterward.
7. **Payoff.** [ON SCREEN: the opening example running correctly.] Say: “Now you can model learners as objects with separate instance state. Here is the result we started with.”
8. **Practice / single CTA.** [ON SCREEN: challenge card and matching HTML exercises.] Say: “Create two instances with independent fields and override one method in a subclass. Pause here and try it before opening the solution.”

## Short to capture inside this lesson

Self-contained moment: **Put per-object mutable data on self inside __init__**.
Replacement opening: 'Why did changing one Python object affect another object?' — hook score 38/100.
First-two-second text: **DATA + BEHAVIOR**. Explain the contrast, show the run, end with the rule that resolves the opening question.
Record a 20–55 second self-contained take within the long lesson. Crop to the relevant code and terminal; do not squeeze the entire desktop into portrait. Loop by returning to the opening input or error on the last frame. Exact clip in/out points await the final timestamped transcript.

## Search package

Target queries (editorial hypotheses, not measured search demand):
- Python Classes for beginners — words covered in title + first two description lines.
- learn Python Classes — words covered in title + first two description lines.
- Python Classes tutorial — words covered in title + first two description lines.

Description draft — replace bracketed fields before upload:

```text
Python Classes for beginners: follow a worked example to model learners as objects with separate instance state.
Learn Python Classes step by step in this Day 21 tutorial from Python 30 Days.

Course lab and mind maps: [ADD YOUR PUBLIC LAB LINK]
Course playlist: [ADD PLAYLIST LINK]
Day 21 example files: [ADD CODE LINK]

[INSERT VERIFIED CHAPTERS AFTER EDITING]

Practice challenge: Create two instances with independent fields and override one method in a subclass.
Preparation: Review the preceding course lessons and run their examples.
This lesson covers: Show two objects with distinct values; Define a class, __init__(), and instance attributes; Write methods and distinguish instance from class attributes; Demonstrate inheritance and method overriding with one small extension.
Use the matching HTML lesson for the full method reference and Level 1–3 exercises.
```

Tags: Python, Python 3, Classes, Python beginners, Python 30 Days. Tags are a small disambiguation aid.

## Chapter labels

Untimed plan; assign boundaries from the final edit, not this outline:
- Compare two separate objects
- Build a class constructor
- Change state with methods
- Extend behavior with inheritance
- Try the student object challenge

Final validation: first chapter 00:00, at least three chapters, ascending boundaries, every chapter including the last at least ten seconds.

## Editing, comments, and retention

- Keep the learner's prediction and the output readable. Retain pauses that allow inspection; remove installation waits and repeated takes. Inspect 'Accidentally sharing mutable class-level state between instances' closely in the final edit.
- Draft creator pin: “Day 21 challenge: Create two instances with independent fields and override one method in a subclass. Which step needs another example?” Replace this with a real recurring learner question when comments arrive.
- After publication, compare the opening promise with the first 30 seconds of the retention curve and inspect the largest drop against the transcript. Choose one revision from the evidence; do not assume every dip is a pacing failure.

## Full source coverage checklist

The main video prioritizes the worked example. Briefly orient viewers to the remaining source topics, and use the HTML as the reference lab; split dense sections into a follow-up rather than silently claiming exhaustive video coverage.

- [ ] Classes and objects
- [ ] Creating a class
- [ ] Creating an object
- [ ] Class constructor
- [ ] Object methods
- [ ] Object default methods
- [ ] Method to modify class default values
- [ ] Inheritance
- [ ] Overriding parent method
- [ ] Exercises
- [ ] Level 1
- [ ] Level 2
- [ ] Level 3

```text
Record next: Day 21 — Python Classes and Objects | Day 21
Opening artifact: Create two Student objects, update one score with a method, and show that the other score stays unchanged.
```

ship it, or change it?
