---
name: dark-olive-broll
description: Design and build explainer-video motion graphics (B-roll) in a dark olive, sage-green, editorial-serif UI style, as animated HTML, Remotion or After Effects specs. Use this skill whenever the user asks for motion graphics, B-roll, animated explainer scenes, lower-third callouts, animated timelines, kinetic text, animated diagrams, source/citation cards, or "make it look like Nick Sarave's videos / that dark green AI explainer style" — even if they never say "skill" or name the style. Also use it to storyboard B-roll from a script or transcript, or to reverse-engineer and extend this look.
---

# Dark Olive B-roll

A complete motion-graphics system reverse-engineered from a 5-minute AI explainer. It reads as a calm dark-mode product UI (think keynote or Linear), not flashy YouTube effects. Everything is built from the same few components, which is why it looks cohesive. **Consistency is the style**: never invent a one-off look.

## Workflow

1. **Get the script or topic.** If the user gives a transcript, split it into beats (one idea per 4–8 seconds). If they give only a topic, write a short beat list and confirm it.
2. **Storyboard.** For each beat pick one scene type from `references/scene-library.md`. Write: scene type, on-screen text (≤ 8 words), the single green-accent element, and which spoken word triggers each reveal.
3. **Choose the output** (ask only if unclear; default to HTML preview):
   - **HTML preview/animation**: start from `assets/scene-kit.html`, add scenes by copying an existing `<section class="scene">` block. This is the default and is what to publish or screen-record.
   - **Remotion/React**: port the tokens and motion rules from `references/design-tokens.md`; one `<Sequence>` per beat.
   - **After Effects / Premiere / CapCut**: deliver the storyboard plus the token and easing values as a build spec.
4. **Build, then check against the Rules below** before presenting.
5. **Offer the next step**: more scenes, a different aspect ratio, or porting to Remotion.

## Non-negotiable rules

- **One accent color.** Sage green `#789858` only. It marks the thing being talked about right now: active timeline node, key word, selected card border, highlighted weights. If everything is green, nothing is.
- **Dark olive, never pure black.** Background `#161911` center fading to `#0f0f0c` at the edges via a radial vignette.
- **Signature headline move:** large editorial serif, with the one key word set in *italic accent green* ("Understand the *history*"). Use at most one italic word per headline. Do not use this on body or pill text.
- **One idea per scene, one new visual every 4–8 seconds**, each element landing on a spoken beat.
- **Dim what is inactive.** Past or upcoming items drop to ~35% opacity; the current one is full white or green.
- **Always show sources.** Real screenshots go in a browser-style frame with a small `● SOURCE · name, date` caption and green underline draw-ons on the quoted sentence.
- **Keep the progress timeline visible** across chapters when the video has a sequence (history, steps, roadmap).
- **Nothing sits still.** Slow push-ins on screenshots, gentle drift on floating pills.
- **Exception:** one scene may break the palette when the topic demands it (the reference used an icy-blue snow scene for "AI winter"). Allow at most one per video and return to olive immediately.

## Components (details in references)

| Component | Use for |
|---|---|
| Statement title | Chapter openers, punchlines |
| Keyword pill | Spoken keywords, asides, questions |
| Glass card | Any grouped content, quotes, code, comparisons |
| Source card | Citing articles, papers, Wikipedia, YouTube |
| Live diagram | Drawing a concept stroke by stroke (network, tree, flow) |
| Progress timeline | Chapter navigation, history, roadmap |
| Orbit / cascade | "Too many things" (jargon cloud), one-to-many branching |
| Compare cards | A vs B, old vs new, ✓ vs ✕ |
| Metaphor visual | Iceberg, funnel, gauge, curve overtaking a line, scribble |
| Slider / counter | Levels of knowledge, big stat ("99%") |
| Typewriter search bar | Questions people ask, curiosity beats |
| Speaker inset | Small rounded headshot in a corner while graphics run |

Read `references/scene-library.md` for exact layouts and timing per scene type, and `references/design-tokens.md` for all colors, type, spacing, easing and the Remotion/CSS snippets.

## Writing on-screen copy

- Sentence case, plain words, ≤ 8 words per element. Pills are fragments ("the problem", "kind of scary"), not sentences.
- Quotes are exact and short; attribute them in the source caption.
- Uppercase letter-spaced eyebrows are reserved for orientation only ("IN THIS VIDEO", "FRANK ROSENBLATT · 1950S"). Do not add one to every scene.

## Quality checklist (run before delivering)

- [ ] Only one accent color is used, and nothing outside the palette appears (except one allowed exception scene)
- [ ] Every headline has at most one italic green word
- [ ] Each scene has one idea and a clear spoken-beat order for reveals
- [ ] Inactive elements are dimmed; current element is clear
- [ ] Sources are cited on screen for any factual claim or screenshot
- [ ] Timeline is present where the content is sequential
- [ ] Safe margins respected (≥ 6% of width), text is readable at 1080p and on phone
- [ ] `prefers-reduced-motion` handled in HTML output

## Known limits

Colors and easing were estimated from sampled frames (about one per 4 seconds), and the fonts are close matches (Instrument Serif / Newsreader and Manrope / Inter), not confirmed. Treat values as a faithful approximation; if the user supplies the original project files or fonts, prefer those.
