# Production workflow — all eleven YouTube skills

## Inputs and working assumptions

The uploaded HTML is the curriculum source. It contains 30 lessons in four modules, mind maps, and exercises. Narration language is confirmed as **English**, and weekly capacity is confirmed as **under four hours**. No channel URL, actual comments, or retention exports were supplied. Whether recordings or other half-made production assets already exist is still unknown.

Still needed: confirm what is already recorded or half-made, and supply three of your own videos for voice matching. The draft uses the confirmed English narration language, but it does not infer a personal voice profile without those samples.

## Skill coverage

| Skill | Applied now | Needs real footage or channel data |
| --- | --- | --- |
| yt-plan | 30-lesson map, confirmed capacity, and two-week production cycle | Existing recordings or half-made assets, measured pilot time, audience activity |
| yt-script | Five scored hooks per lesson; 30 beat sheets; full Day 1 spoken draft in English | Three voice samples; full spoken drafts for Days 2–30 after voice matching |
| yt-package | Ten scored title/thumbnail pairs per lesson; top three reported; two editorial options | Finished thumbnail graphics and real audience response |
| yt-viral | Five sourced public videos compared against their same-channel sample median | Broader current sample for the intended English-speaking audience |
| yt-seo | Description, tags, and three query hypotheses per lesson | Public course, playlist, and code URLs |
| yt-shorts | One planned moment per lesson; five ranked pilot candidates below | Recorded spans and exact timecodes |
| yt-chapters | Lesson-specific chapter labels | Final edited SRT/VTT and actual video duration |
| yt-edit | Course-specific editing brief and tool command | Timestamped rough-cut transcript for a real edit decision list |
| yt-comment | Reply patterns, triage process, draft creator pins | Actual comment batch and recurring-question counts |
| yt-retention | Data collection and one-fix review workflow | Real export, units, video duration, final transcript |
| yt-audit | Pre-launch review of the supplied curriculum and draft packaging | Channel URL, last ten uploads, thumbnails, opening clips, analytics |

Scores are reproducible tool outputs, not predictions. Pending analyses are not represented as completed analyses.

## 1. Capacity-based publishing plan — yt-plan

**Confirmed capacity: under four hours per week. Planned load: no more than three hours per week.** The remaining capacity is buffer, not pre-committed production time. Use a two-week cycle capped at six planned hours per main lesson. One main lesson every two weeks makes the 30 core lessons a roughly 60-week production and release run, excluding breaks. “30 Days” labels the learning sequence; it does not require thirty consecutive publishing days.

Use audience analytics to choose actual publication days. Until those exist, choose consistent slots that fit production, without claiming a universal best upload time.

| Cycle point | Work / format | Working title | Promise | What exists already | Budget |
| --- | --- | --- | --- | --- | --- |
| Week 1, work block 1 | Outline and demonstration prep | Run Your First Python File | Run and explain a saved file | HTML, Day 1 script, hook and title scores; status of any existing recording is unknown | 1 h |
| Week 1, work block 2 | Rehearse and prepare capture | Run Your First Python File | Show the result, reproduce it, and repair one error | Script and demonstration plan | 0.75 h |
| Week 1, work block 3 | Record anchor | Run Your First Python File | Capture the working example and learner exercise | Recording may already exist in whole or part; confirm before re-recording | 1.25 h |
| Week 2, work block 1 | Rough edit | Day 1 anchor | Keep code, output, correction, and challenge readable | Recorded footage from Week 1 or a confirmed reusable asset | 1.5 h |
| Week 2, work block 2 | Finish and package | Day 1 anchor | Deliver a clear lesson with accurate title, thumbnail, and description | Package drafts and score files exist; final-media status is unknown | 1 h |
| Week 2, publication block | Quality check, publish, and review replies | Run Your First Python File | Finish the first working lab | Requires the completed anchor; actual publication slot remains analytics-led | 0.5 h |

This baseline commits to **one main lesson every two weeks**, not three uploads per week. An optional Short can be cut from the anchor only when the lesson finishes below its six-hour cap or when time is deliberately reallocated from another task. It is not an extra commitment and must not push either week above three planned hours. Bank usable moments rather than promising a Short for every cycle.

**If a week slips:** move the unfinished anchor work into the next available block and extend the cycle. Drop the optional Short first. Protect the anchor's working example, correction, and exercise rather than compressing them to preserve cadence.

For each two-week cycle, take the next row from [the 30-video map](30-video-plan.md). Measure the Day 1 pilot's actual preparation, recording, editing, packaging, and publication time. Replace estimates with the measured average after enough completed lessons to reveal the workload, and extend the cycle if six hours is not workable. Days 14, 24, and the web/database/API lessons may need more production time, a longer cycle, or a second part.

## 2. Script and packaging rules — yt-script / yt-package

1. Show the real output or error before the course introduction.
2. Use the mind map for a short orientation and recap; keep most screen time on code and output.
3. Ask for a prediction, run the code, explain the result, then vary one input.
4. Demonstrate one misconception explicitly, rather than reading a list of definitions.
5. End on one practice request. Avoid a combined subscribe/like/comment/share close.

Each brief includes ten title candidates checked against its thumbnail words and five scored hooks. All candidates and individual hook properties are preserved in [all-scores.json](scores/all-scores.json). The linter uses approximate display-width rules and simple word matching. It does not evaluate teaching quality or the rendered thumbnail. Keep useful lesson-specific wording even if a generic candidate scores higher.

Thumbnail system: charcoal background, yellow three-word-or-shorter label, blue code accent, one enlarged input/output contrast. A small course-day badge can provide navigation, but the result must remain the dominant element. Titles should lead with the concept or outcome rather than identical “Day N” prefixes.

## 3. Five pilot Shorts candidates — yt-shorts

These are **ranked editorially from the draft script**, not extracted recordings. In/out timestamps are pending. Target 20–55 seconds each; preserve the self-contained explanation. Replacement openings are scored in [short-hook-scores.json](scores/short-hook-scores.json).

| Rank | Source section | New first spoken line | First-two-second text | Closing rule / loop point |
| --- | --- | --- | --- | --- |
| 1 | 9: Resolve the opening puzzle | Why does your Python file show nothing when the shell shows 30? | WHERE DID IT GO? | End on “Use print when your script needs to show the result,” then return to the quiet file |
| 2 | 5: Know which prompt | Before you run your Python file, check these 3 symbols: are you inside the wrong prompt? | WRONG WINDOW? | Finish with exit(), reveal the terminal prompt, then return to >>> |
| 3 | 8: Save and run | Your Python code changed, but the output did not. Which file did you run? | OLD RESULT | Show save, filename, and folder checks; return to the old output |
| 4 | 7: Break one line | Your first Python syntax error can start with 1 missing parenthesis. Can you spot it? | FIND THE GAP | Add the parenthesis, show the result, then reset to the broken line |
| 5 | 10: Preview types | Why does Python treat 30 and the text '30' as different values? | SAME LOOK, DIFFERENT | End on the two different type results, then return to the matching-looking values |

For candidate 5, record the additional `type('30')` comparison during section 10. It is a planned extra capture, not a claim that the present script already contains that exact comparison.

Vertical framing: crop to a few lines and their output. Reframe the editor and terminal as stacked panels if necessary. Keep the cursor and the relevant prompt within the crop. Do not shrink the whole desktop. Read the replacement opening at the start of each standalone take so it does not begin with “as we saw earlier.”

If the anchor recording naturally includes them within its six-hour production cap, capture candidates 1–3 in the pilot session; candidates 4–5 are backups. Editing or publishing a Short uses spare or explicitly reallocated time, not an added weekly commitment. After transcription, rerank the actual spans by clarity and completeness, not by hook score alone.

## 4. Editing and chapters — yt-edit / yt-chapters

### Course-specific edit brief

- Keep readable output on screen long enough to compare it with the code.
- Preserve deliberate prediction pauses. A silence detector cannot tell a useful coding pause from dead air.
- Remove repeated explanations, failed retakes, installation waits, and irrelevant mouse travel.
- Keep the wrong line and its correction in the same shot where possible.
- When referring to a type, a key, or an interpreter, highlight the exact item rather than adding unrelated B-roll.
- Use a short “try this” card where the learner should pause the video.

Export a timestamped rough-cut transcript to `youtube-course/inputs/day-01-rough.srt`. From the workspace root, run:

```powershell
python .opencode/skills/yt-edit/deadair.py youtube-course/inputs/day-01-rough.srt --floor 0.35 --json
```

Review each proposed DEAD, FILLER, and REPEAT cut against the footage. The tool proposes cuts; it does not edit media. After applying edits, export a **new final transcript**, since all downstream timestamps must follow the final cut:

```powershell
python .opencode/skills/yt-chapters/chapters.py youtube-course/inputs/day-01-final.srt --target 5 --json
```

Retitle the generated boundaries using the lesson's chapter labels. Confirm the first label is `00:00`, at least three chapters exist, and each lasts at least ten seconds, including the final one. The installed tool prints `0:00`; normalize that first label to `00:00` when preparing the description. Inspect boundaries visually: a vocabulary shift is only a candidate section boundary.

No edit list or validated timed chapters have been fabricated from the written outline.

## 5. Descriptions and discovery — yt-seo

Every lesson brief includes three query hypotheses, a description draft, and a short tag list. All 90 query-word coverage checks passed against the respective title and first two description lines. This checks wording only; search demand and ranking remain unmeasured.

Replace the public lab, playlist, and code link placeholders. A local `C:\...` file path is not a viewer-download link. Put verified chapters beneath the resources, and link the previous/next lesson where useful. Write the first lines naturally for the confirmed English narration and intended audience; do not distort them solely to preserve keyword matches.

## 6. Comments — yt-comment

**Actual comments received: none.** Therefore there are no measured triage counts or real learner comments to pin. Once a batch arrives, count Questions / Corrections / Praise / Bait before drafting replies. Track repeated questions as candidates for the inexpensive follow-up.

These are **hypothetical reply patterns**, each under 30 words:

| Category | Example incoming comment | Draft reply |
| --- | --- | --- |
| Question | “I see >>>. Where do I type python hello.py?” | “Type exit() to leave Python, then run python hello.py at the terminal prompt. Is your terminal in the folder containing the file?” |
| Question | “My file runs but shows nothing.” | “Use print() to display a value in a script. The interactive shell displays expression results automatically.” |
| Correction | “My installation screen looks different.” | “Thanks for flagging it. Installer screens vary. Which operating system and installation method are you using?” |
| Praise | “The shell versus file example finally made sense.” | “Glad that comparison helped. Try changing the calculation in both places and predicting what each one displays.” |
| Bait | Insult with no actionable question | No reply. |

Suggested creator pin for Day 1:

```text
Day 1 challenge: save and run your own greeting file. If you get stuck, share the command you ran and the exact error text.
```

When real comments arrive, pin **one recurring setup question with a useful answer**, rather than automatically pinning praise. Verify technical corrections and acknowledge them plainly.

## 7. Retention review — yt-retention

After the video has usable audience data, supply its retention export, final duration in seconds, and final SRT. Record the export date and traffic context. A small early sample may not support a firm diagnosis.

The installed reader expects at least eight data points with position and audience percentage. It guesses a percentage axis when the maximum position is at most 100.5. To remove that ambiguity, prepare the first column as **0–100 elapsed-video percentage**, and pass the real duration. The second column should be audience-retention percentage, not a 0–1 fraction. Confirm the exported units before conversion.

```powershell
# Replace 600 with the actual final duration; it is only an example here.
python .opencode/skills/yt-retention/retention.py youtube-course/inputs/day-01-retention.csv --duration 600 --transcript youtube-course/inputs/day-01-final.srt --json
```

Review opening loss, isolated drops, and the middle slope. Choose **one** largest supported issue and one action. Example conditional diagnosis: if a drop aligns with a long installation wait, shorten that wait in the next lesson. If a drop aligns with a confusing new concept, improve the explanation. Do not treat a heuristic threshold as proof of cause or assume every decline means editing is the problem.

Output format when real data is available:

```text
Largest observed leak: [time interval and measured change]
What was on screen / being said: [verified from the final cut]
One proposed change: [specific revision]
How we will check it: [comparable follow-up measurement]
```

## 8. Pre-launch audit — yt-audit

**Single biggest fix: replace topic-list openings with a visible learner result.** In the Day 1 pilot cycle, record the working file first and build its opening around the shell/file contrast. That makes the first lesson deliver an observable outcome before asking the viewer to sit through setup.

Three strengths to preserve from the supplied artifact:

1. The 30-day sequence provides a clear path from language basics to a small API.
2. The mind maps give you a ready-made visual recap and transition system.
3. The three exercise levels support practice beyond passive watching.

Defer a channel rebrand or any faster publishing commitment until the pilot's production time and learner response are known. Neither is necessary to test the lesson format.

This is a pre-launch curriculum/format review. A channel audit still needs the channel URL, last ten titles and thumbnails, first fifteen seconds of three recent uploads, upload history, and available retention data. The last ten draft lesson titles were included in the packaging checks, but they are not actual channel uploads.

## 9. Recording accuracy notes from the course

- Day 1 includes historical Python version examples. Record the current supported interpreter you actually use and explain command differences accurately.
- Preview environment isolation on Day 20 before package installation; keep Day 23 as the dedicated environment lesson.
- Day 24 covers substantially more material than a short introductory statistics video. Separate core demonstration from reference coverage or make an explicit second part.
- Day 26's Heroku account/deployment screens are historical instructions to revalidate before recording. The first web-video promise is a working local Flask page.
- Day 27's Atlas screens and plan labels should match the recording date. Show the actual current workflow rather than narrating an old screenshot.
- Treat the Day 29 API as a learning project; describe exactly which behaviors the demonstration implements.

```text
Next: inventory recordings and half-made assets, supply three voice samples, produce the Day 1 pilot within the two-week cycle, and record its actual hours before supplying the rough transcript for the first real edit pass.
```

ship it, or change it?
