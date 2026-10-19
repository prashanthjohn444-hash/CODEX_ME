# Day 19 — Python Files

Source: **Day 19 — File Handling**, Module 3 · Intermediate. Extracted text: [source](../source/day-19.txt).

Status: production brief; English narration confirmed, personal voice matching pending. No recording or performance data supplied. Plan one main lesson every two weeks within the confirmed under-four-hour weekly capacity.
Planning target: **8–15 minutes**, including live typing, demonstrations, and practice pauses. This is not a measured runtime.

## Promise and proof

After this lesson, the learner can **save and reload learner data using text, JSON, and CSV**.
Opening proof: Write a learner record to JSON, close the program, and load the record in a new run.
Misconception to resolve: Opening an existing file with w when you intended to append.

## Packaging

Editorial recommendation: **Python Files: Save Your Data | Day 19** — linter 100/100.
Keep the topic/outcome early and the course-day label at the end. The recommendation uses lesson fit as well as the linter; it need not be the highest numeric score.

Top three by linter (ties preserve candidate order):

| Title | Score | Specific issues |
| --- | --- | --- |
| Python Files: Save Your Data  /  Day 19 | 100 | No linter flags |
| Python Files for Beginners  /  Day 19 | 100 | No linter flags |
| Learn Python Files  /  Day 19 | 100 | No linter flags |

Second editorial option: Python Files for Beginners | Day 19
Recommended-title flags: None from the tool.
Thumbnail text: **STILL THERE**.
Thumbnail brief: dark charcoal background, one enlarged code/output contrast from this demo: Write a learner record to JSON, close the program, and load the record in a new run. Yellow text, blue code accent; hide tiny editor chrome. Keep text to the stated three words or fewer. If a face is used, show a natural questioning expression facing the output; a faceless layout is equally workable. Check readability at small feed size.

## Hook options — five scored, top two shown

Scores are writing heuristics, not predictions of views or retention. Use the two below as reading options; keep the one that sounds natural and matches the opening shot.

| Hook | Verdict | Specificity | Address | Stakes | Curiosity | Brevity | Detected formula |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Before you copy this Python example, predict what will happen. Your Day 19 lab starts with files. | 70 (WORKABLE) | 74 | 96 | 62 | 58 | 100 | The Warning |
| Why does your Python file lose its old contents when you save again? | 57 (WORKABLE) | 40 | 96 | 48 | 59 | 100 | The Question |

Top-scoring hook's intended structure: **The Warning — avoid passive copying**. It introduces the lesson's actual demonstration or asks the question the demonstration resolves. The detector's keyword label may differ.

## Script beat sheet

These are recording directions, not a word-for-word script. See the separate Day 1 pilot for a spoken draft.
1. **Hook / first ~15 seconds.** [ON SCREEN: the actual output or error from the demo.] Say one selected hook, then show evidence: Write a learner record to JSON, close the program, and load the record in a new run.
2. **Turn / next ~30 seconds.** [ON SCREEN: editor and a compact branch of this day's mind map.] Say: 'We will save and reload learner data using text, JSON, and CSV. First, predict what this example will do.'
3. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Restart the script and show saved data surviving. Ask for a prediction before running; explain the observed result afterward.
4. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Use with open(), explicit encoding, and read methods. Ask for a prediction before running; explain the observed result afterward.
5. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Contrast write and append with a disposable example file. Ask for a prediction before running; explain the observed result afterward.
6. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Serialize JSON, read CSV, and position XLSX/XML as separate file formats with their own tools. Ask for a prediction before running; explain the observed result afterward.
7. **Payoff.** [ON SCREEN: the opening example running correctly.] Say: “Now you can save and reload learner data using text, JSON, and CSV. Here is the result we started with.”
8. **Practice / single CTA.** [ON SCREEN: challenge card and matching HTML exercises.] Say: “Save a dictionary as JSON and reload it; append a log entry without overwriting previous entries. Pause here and try it before opening the solution.”

## Short to capture inside this lesson

Self-contained moment: **w replaces file contents; a appends**.
Replacement opening: 'Why does your Python file lose its old contents when you save again?' — hook score 57/100.
First-two-second text: **STILL THERE**. Explain the contrast, show the run, end with the rule that resolves the opening question.
Record a 20–55 second self-contained take within the long lesson. Crop to the relevant code and terminal; do not squeeze the entire desktop into portrait. Loop by returning to the opening input or error on the last frame. Exact clip in/out points await the final timestamped transcript.

## Search package

Target queries (editorial hypotheses, not measured search demand):
- Python Files for beginners — words covered in title + first two description lines.
- learn Python Files — words covered in title + first two description lines.
- Python Files tutorial — words covered in title + first two description lines.

Description draft — replace bracketed fields before upload:

```text
Python Files for beginners: follow a worked example to save and reload learner data using text, JSON, and CSV.
Learn Python Files step by step in this Day 19 tutorial from Python 30 Days.

Course lab and mind maps: [ADD YOUR PUBLIC LAB LINK]
Course playlist: [ADD PLAYLIST LINK]
Day 19 example files: [ADD CODE LINK]

[INSERT VERIFIED CHAPTERS AFTER EDITING]

Practice challenge: Save a dictionary as JSON and reload it; append a log entry without overwriting previous entries.
Preparation: Review the preceding course lessons and run their examples.
This lesson covers: Restart the script and show saved data surviving; Use with open(), explicit encoding, and read methods; Contrast write and append with a disposable example file; Serialize JSON, read CSV, and position XLSX/XML as separate file formats with their own tools.
Use the matching HTML lesson for the full method reference and Level 1–3 exercises.
```

Tags: Python, Python 3, Files, Python beginners, Python 30 Days. Tags are a small disambiguation aid.

## Chapter labels

Untimed plan; assign boundaries from the final edit, not this outline:
- Keep data between runs
- Read files with context
- Choose write or append
- Save structured JSON data
- Try the reload challenge

Final validation: first chapter 00:00, at least three chapters, ascending boundaries, every chapter including the last at least ten seconds.

## Editing, comments, and retention

- Keep the learner's prediction and the output readable. Retain pauses that allow inspection; remove installation waits and repeated takes. Inspect 'Opening an existing file with w when you intended to append' closely in the final edit.
- Draft creator pin: “Day 19 challenge: Save a dictionary as JSON and reload it; append a log entry without overwriting previous entries. Which step needs another example?” Replace this with a real recurring learner question when comments arrive.
- After publication, compare the opening promise with the first 30 seconds of the retention curve and inspect the largest drop against the transcript. Choose one revision from the evidence; do not assume every dip is a pacing failure.

## Full source coverage checklist

The main video prioritizes the worked example. Briefly orient viewers to the remaining source topics, and use the HTML as the reference lab; split dense sections into a follow-up rather than silently claiming exhaustive video coverage.

- [ ] File handling
- [ ] open() modes
- [ ] Opening files for reading
- [ ] read()
- [ ] readline()
- [ ] readlines()
- [ ] splitlines()
- [ ] with
- [ ] Opening files for writing and updating
- [ ] write() / append
- [ ] Deleting files
- [ ] File types
- [ ] File with txt extension
- [ ] File with json extension
- [ ] Changing JSON to dictionary
- [ ] Changing dictionary to JSON
- [ ] Saving as JSON file
- [ ] File with csv extension
- [ ] File with xlsx extension
- [ ] File with xml extension
- [ ] Exercises
- [ ] Level 1
- [ ] Level 2
- [ ] Level 3

```text
Record next: Day 19 — Python Files: Save Your Data | Day 19
Opening artifact: Write a learner record to JSON, close the program, and load the record in a new run.
```

ship it, or change it?
