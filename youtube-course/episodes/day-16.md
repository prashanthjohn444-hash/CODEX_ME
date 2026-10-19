# Day 16 — Python datetime

Source: **Day 16 — Date and Time**, Module 3 · Intermediate. Extracted text: [source](../source/day-16.txt).

Status: production brief; English narration confirmed, personal voice matching pending. No recording or performance data supplied. Plan one main lesson every two weeks within the confirmed under-four-hour weekly capacity.
Planning target: **8–15 minutes**, including live typing, demonstrations, and practice pauses. This is not a measured runtime.

## Promise and proof

After this lesson, the learner can **parse, format, and subtract dates**.
Opening proof: Parse '2026-10-08' with strptime(), format it for display, and calculate the interval to another fixed date.
Misconception to resolve: Confusing the input format with the desired display format.

## Packaging

Editorial recommendation: **Python datetime: Parse Dates | Day 16** — linter 100/100.
Keep the topic/outcome early and the course-day label at the end. The recommendation uses lesson fit as well as the linter; it need not be the highest numeric score.

Top three by linter (ties preserve candidate order):

| Title | Score | Specific issues |
| --- | --- | --- |
| Python datetime: Parse Dates  /  Day 16 | 100 | No linter flags |
| Python datetime for Beginners  /  Day 16 | 100 | No linter flags |
| Learn Python datetime  /  Day 16 | 100 | No linter flags |

Second editorial option: Python datetime for Beginners | Day 16
Recommended-title flags: None from the tool.
Thumbnail text: **TEXT TO TIME**.
Thumbnail brief: dark charcoal background, one enlarged code/output contrast from this demo: Parse '2026-10-08' with strptime(), format it for display, and calculate the interval to another fixed date. Yellow text, blue code accent; hide tiny editor chrome. Keep text to the stated three words or fewer. If a face is used, show a natural questioning expression facing the output; a faceless layout is equally workable. Check readability at small feed size.

## Hook options — five scored, top two shown

Scores are writing heuristics, not predictions of views or retention. Use the two below as reading options; keep the one that sounds natural and matches the opening shot.

| Hook | Verdict | Specificity | Address | Stakes | Curiosity | Brevity | Detected formula |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Before you copy this Python example, predict what will happen. Your Day 16 lab starts with datetime. | 70 (WORKABLE) | 74 | 96 | 62 | 58 | 100 | The Warning |
| Why does your Python date parse fail even when the date looks right? | 55 (WORKABLE) | 40 | 76 | 48 | 59 | 100 | The Question |

Top-scoring hook's intended structure: **The Warning — avoid passive copying**. It introduces the lesson's actual demonstration or asks the question the demonstration resolves. The detector's keyword label may differ.

## Script beat sheet

These are recording directions, not a word-for-word script. See the separate Day 1 pilot for a spoken draft.
1. **Hook / first ~15 seconds.** [ON SCREEN: the actual output or error from the demo.] Say one selected hook, then show evidence: Parse '2026-10-08' with strptime(), format it for display, and calculate the interval to another fixed date.
2. **Turn / next ~30 seconds.** [ON SCREEN: editor and a compact branch of this day's mind map.] Say: 'We will parse, format, and subtract dates. First, predict what this example will do.'
3. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Show a date string becoming a datetime object. Ask for a prediction before running; explain the observed result afterward.
4. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Inspect year, month, day, and time components. Ask for a prediction before running; explain the observed result afterward.
5. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Contrast strptime() with strftime() and use the format-code reference. Ask for a prediction before running; explain the observed result afterward.
6. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Subtract dates and add timedelta without manually counting month lengths. Ask for a prediction before running; explain the observed result afterward.
7. **Payoff.** [ON SCREEN: the opening example running correctly.] Say: “Now you can parse, format, and subtract dates. Here is the result we started with.”
8. **Practice / single CTA.** [ON SCREEN: challenge card and matching HTML exercises.] Say: “Parse two known dates and report their difference in days, including a month boundary. Pause here and try it before opening the solution.”

## Short to capture inside this lesson

Self-contained moment: **strptime parses; strftime formats**.
Replacement opening: 'Why does your Python date parse fail even when the date looks right?' — hook score 55/100.
First-two-second text: **TEXT TO TIME**. Explain the contrast, show the run, end with the rule that resolves the opening question.
Record a 20–55 second self-contained take within the long lesson. Crop to the relevant code and terminal; do not squeeze the entire desktop into portrait. Loop by returning to the opening input or error on the last frame. Exact clip in/out points await the final timestamped transcript.

## Search package

Target queries (editorial hypotheses, not measured search demand):
- Python datetime for beginners — words covered in title + first two description lines.
- learn Python datetime — words covered in title + first two description lines.
- Python datetime tutorial — words covered in title + first two description lines.

Description draft — replace bracketed fields before upload:

```text
Python datetime for beginners: follow a worked example to parse, format, and subtract dates.
Learn Python datetime step by step in this Day 16 tutorial from Python 30 Days.

Course lab and mind maps: [ADD YOUR PUBLIC LAB LINK]
Course playlist: [ADD PLAYLIST LINK]
Day 16 example files: [ADD CODE LINK]

[INSERT VERIFIED CHAPTERS AFTER EDITING]

Practice challenge: Parse two known dates and report their difference in days, including a month boundary.
Preparation: Review the preceding course lessons and run their examples.
This lesson covers: Show a date string becoming a datetime object; Inspect year, month, day, and time components; Contrast strptime() with strftime() and use the format-code reference; Subtract dates and add timedelta without manually counting month lengths.
Use the matching HTML lesson for the full method reference and Level 1–3 exercises.
```

Tags: Python, Python 3, datetime, Python beginners, Python 30 Days. Tags are a small disambiguation aid.

## Chapter labels

Untimed plan; assign boundaries from the final edit, not this outline:
- Turn text into dates
- Inspect date and time parts
- Choose the matching format
- Calculate a date difference
- Try the deadline challenge

Final validation: first chapter 00:00, at least three chapters, ascending boundaries, every chapter including the last at least ten seconds.

## Editing, comments, and retention

- Keep the learner's prediction and the output readable. Retain pauses that allow inspection; remove installation waits and repeated takes. Inspect 'Confusing the input format with the desired display format' closely in the final edit.
- Draft creator pin: “Day 16 challenge: Parse two known dates and report their difference in days, including a month boundary. Which step needs another example?” Replace this with a real recurring learner question when comments arrive.
- After publication, compare the opening promise with the first 30 seconds of the retention curve and inspect the largest drop against the transcript. Choose one revision from the evidence; do not assume every dip is a pacing failure.

## Full source coverage checklist

The main video prioritizes the worked example. Briefly orient viewers to the remaining source topics, and use the HTML as the reference lab; split dense sections into a follow-up rather than silently claiming exhaustive video coverage.

- [ ] Python datetime
- [ ] Getting datetime information
- [ ] Formatting date output using strftime
- [ ] Full strftime format codes
- [ ] String to time using strptime
- [ ] Using date from datetime
- [ ] Time objects to represent time
- [ ] Difference between two points in time
- [ ] Difference using timedelta
- [ ] Exercises
- [ ] Level 1
- [ ] Level 2
- [ ] Level 3

```text
Record next: Day 16 — Python datetime: Parse Dates | Day 16
Opening artifact: Parse '2026-10-08' with strptime(), format it for display, and calculate the interval to another fixed date.
```

ship it, or change it?
