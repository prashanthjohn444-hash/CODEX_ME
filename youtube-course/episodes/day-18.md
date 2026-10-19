# Day 18 — Python Regex

Source: **Day 18 — Regular Expressions**, Module 3 · Intermediate. Extracted text: [source](../source/day-18.txt).

Status: production brief; English narration confirmed, personal voice matching pending. No recording or performance data supplied. Plan one main lesson every two weeks within the confirmed under-four-hour weekly capacity.
Planning target: **8–15 minutes**, including live typing, demonstrations, and practice pauses. This is not a measured runtime.

## Promise and proof

After this lesson, the learner can **extract and replace simple text patterns with re**.
Opening proof: Extract sample order numbers from a short log and replace repeated whitespace with a single space.
Misconception to resolve: Using match() when the desired pattern begins later in the text.

## Packaging

Editorial recommendation: **Python Regex: Find Patterns | Day 18** — linter 100/100.
Keep the topic/outcome early and the course-day label at the end. The recommendation uses lesson fit as well as the linter; it need not be the highest numeric score.

Top three by linter (ties preserve candidate order):

| Title | Score | Specific issues |
| --- | --- | --- |
| Python Regex: Find Patterns  /  Day 18 | 100 | No linter flags |
| Python Regex for Beginners  /  Day 18 | 100 | No linter flags |
| Learn Python Regex  /  Day 18 | 100 | No linter flags |

Second editorial option: Python Regex for Beginners | Day 18
Recommended-title flags: None from the tool.
Thumbnail text: **EXTRACT THE MATCH**.
Thumbnail brief: dark charcoal background, one enlarged code/output contrast from this demo: Extract sample order numbers from a short log and replace repeated whitespace with a single space. Yellow text, blue code accent; hide tiny editor chrome. Keep text to the stated three words or fewer. If a face is used, show a natural questioning expression facing the output; a faceless layout is equally workable. Check readability at small feed size.

## Hook options — five scored, top two shown

Scores are writing heuristics, not predictions of views or retention. Use the two below as reading options; keep the one that sounds natural and matches the opening shot.

| Hook | Verdict | Specificity | Address | Stakes | Curiosity | Brevity | Detected formula |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Before you copy this Python example, predict what will happen. Your Day 18 lab starts with regex. | 70 (WORKABLE) | 74 | 96 | 62 | 58 | 100 | The Warning |
| I'm going to show you regex in Python, with the result on screen before we explain the code. | 53 (WEAK) | 40 | 76 | 48 | 41 | 100 | The Reveal |

Top-scoring hook's intended structure: **The Warning — avoid passive copying**. It introduces the lesson's actual demonstration or asks the question the demonstration resolves. The detector's keyword label may differ.

## Script beat sheet

These are recording directions, not a word-for-word script. See the separate Day 1 pilot for a spoken draft.
1. **Hook / first ~15 seconds.** [ON SCREEN: the actual output or error from the demo.] Say one selected hook, then show evidence: Extract sample order numbers from a short log and replace repeated whitespace with a single space.
2. **Turn / next ~30 seconds.** [ON SCREEN: editor and a compact branch of this day's mind map.] Say: 'We will extract and replace simple text patterns with re. First, predict what this example will do.'
3. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Highlight desired matches before showing the pattern. Ask for a prediction before running; explain the observed result afterward.
4. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Introduce raw strings and the re module. Ask for a prediction before running; explain the observed result afterward.
5. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Compare match(), search(), findall(), sub(), and split(). Ask for a prediction before running; explain the observed result afterward.
6. **Teaching beat.** [ON SCREEN: the relevant code and output together; highlight only the changed line.] Build character classes and quantifiers before previewing groups, flags, and lookaheads. Ask for a prediction before running; explain the observed result afterward.
7. **Payoff.** [ON SCREEN: the opening example running correctly.] Say: “Now you can extract and replace simple text patterns with re. Here is the result we started with.”
8. **Practice / single CTA.** [ON SCREEN: challenge card and matching HTML exercises.] Say: “Find all numeric order IDs and explain the difference between search(), match(), and findall(). Pause here and try it before opening the solution.”

## Short to capture inside this lesson

Self-contained moment: **match() starts at the beginning; search() looks through the string**.
Replacement opening: 'Why does your Python regex miss a pattern that is clearly there?' — hook score 44/100.
First-two-second text: **EXTRACT THE MATCH**. Explain the contrast, show the run, end with the rule that resolves the opening question.
Record a 20–55 second self-contained take within the long lesson. Crop to the relevant code and terminal; do not squeeze the entire desktop into portrait. Loop by returning to the opening input or error on the last frame. Exact clip in/out points await the final timestamped transcript.

## Search package

Target queries (editorial hypotheses, not measured search demand):
- Python Regex for beginners — words covered in title + first two description lines.
- learn Python Regex — words covered in title + first two description lines.
- Python Regex tutorial — words covered in title + first two description lines.

Description draft — replace bracketed fields before upload:

```text
Python Regex for beginners: follow a worked example to extract and replace simple text patterns with re.
Learn Python Regex step by step in this Day 18 tutorial from Python 30 Days.

Course lab and mind maps: [ADD YOUR PUBLIC LAB LINK]
Course playlist: [ADD PLAYLIST LINK]
Day 18 example files: [ADD CODE LINK]

[INSERT VERIFIED CHAPTERS AFTER EDITING]

Practice challenge: Find all numeric order IDs and explain the difference between search(), match(), and findall().
Preparation: Review the preceding course lessons and run their examples.
This lesson covers: Highlight desired matches before showing the pattern; Introduce raw strings and the re module; Compare match(), search(), findall(), sub(), and split(); Build character classes and quantifiers before previewing groups, flags, and lookaheads.
Use the matching HTML lesson for the full method reference and Level 1–3 exercises.
```

Tags: Python, Python 3, Regex, Python beginners, Python 30 Days. Tags are a small disambiguation aid.

## Chapter labels

Untimed plan; assign boundaries from the final edit, not this outline:
- Mark the text you need
- Choose a matching function
- Build a small pattern
- Replace and group matches
- Try the order ID challenge

Final validation: first chapter 00:00, at least three chapters, ascending boundaries, every chapter including the last at least ten seconds.

## Editing, comments, and retention

- Keep the learner's prediction and the output readable. Retain pauses that allow inspection; remove installation waits and repeated takes. Inspect 'Using match() when the desired pattern begins later in the text' closely in the final edit.
- Draft creator pin: “Day 18 challenge: Find all numeric order IDs and explain the difference between search(), match(), and findall(). Which step needs another example?” Replace this with a real recurring learner question when comments arrive.
- After publication, compare the opening promise with the first 30 seconds of the retention curve and inspect the largest drop against the transcript. Choose one revision from the evidence; do not assume every dip is a pacing failure.

## Full source coverage checklist

The main video prioritizes the worked example. Briefly orient viewers to the remaining source topics, and use the HTML as the reference lab; split dense sections into a follow-up rather than silently claiming exhaustive video coverage.

- [ ] Regular expressions
- [ ] The re module
- [ ] Methods in the re module
- [ ] re.match()
- [ ] re.search()
- [ ] re.findall()
- [ ] re.sub()
- [ ] re.split()
- [ ] Writing RegEx patterns
- [ ] Regular expression cheat sheet
- [ ] Square bracket
- [ ] Escape character
- [ ] One or more times (+)
- [ ] Period (.)
- [ ] Zero or more times (*)
- [ ] Zero or one time (?)
- [ ] Quantifier in RegEx
- [ ] Caret (^)
- [ ] Groups, lookaheads, flags
- [ ] Exercises
- [ ] Level 1
- [ ] Level 2
- [ ] Level 3

```text
Record next: Day 18 — Python Regex: Find Patterns | Day 18
Opening artifact: Extract sample order numbers from a short log and replace repeated whitespace with a single space.
```

ship it, or change it?
