# Scene library

Contents: 1 Statement · 2 Keyword pills · 3 Quote card · 4 Source screenshot · 5 Live diagram · 6 Compare cards · 7 Orbit of jargon · 8 Fan-out cascade · 9 Metaphor visuals · 10 Slider and counter · 11 Search bar · 12 Speaker inset · 13 Chapter timeline · 14 Resource list · 15 Closing overview · Pacing recipes · Storyboard template

Times are relative to scene start. "Beat" means the spoken word that triggers the reveal. Layout positions are in % of the 16:9 frame.

## 1. Statement title
Big serif line centered at ~28% from the top, key word in italic accent. Words reveal left to right; the italic word lands ~0.6s after the rest. Optional uppercase eyebrow above. Examples: "Understand the *history*", "After the *AI winter*", "The rest is *history*", "2011, 2012", "People started talking" (with a small accent icon above).
Variants: big year/number alone (7–9cqw) with a small eyebrow ("WHERE WE START" over "1950s").

## 2. Keyword pills
Dark pills with a dot or icon. Place near the visual they annotate, appearing on the beat of the spoken keyword. Use for asides and questions ("what was he trying to solve?" with a ? icon), highlights ("a tremendous amount of excitement"), and labels ("kind of scary" over "myself included", stacked, second pill dimmer). Max 3 pills visible at once unless it is the orbit scene.

## 3. Quote card
Glass card, left/right 14%, serif quote at 3.2cqw. Underline the key phrases with green draw-on lines as the speaker reaches them (0.9s each). Source caption below. If a person is quoted, show a small portrait on the left with name and role in uppercase caption beneath.

## 4. Source screenshot
Browser-framed screenshot centered at ~55% width. Entrance: fade in dimmed, then brighten. Slow push-in toward the relevant text. Underline the cited sentence in green. Caption `● SOURCE · Publisher, date` above. A stat card ("99%" with a short label) can slide in from the right while the page dims.
Variants: Wikipedia page with a portrait card overlapping its corner; a paper (arXiv) with floating logo tiles around it; YouTube thumbnail cards with play button, title, channel and year in the footer.

## 5. Live diagram
Dark scene, thin white 1.6px strokes, circular nodes (dark fill, white outline). Build order: nodes (100ms apart) → connecting lines draw on (≈200ms apart) → center operator glows green (Σ) → labels (weights) fade in and turn green as the narrator names them → output node. Pills annotate on the side. Use for neural nets, decision trees (IF/THEN boxes with branches drawing downward), pipelines, hub-and-spoke flows.

## 6. Compare cards
Two glass cards side by side with a status badge each (green ✓ / red ✕). The active card gets the accent border. Footer pills explain each ("worked for some problems", "not based on neural networks"). Code-like card content uses mono at ~1.9cqw. Optionally animate a file name label above ("program.py").

## 7. Orbit of jargon
Central icon tile (person) in accent. 8–12 pills float around in a rough circle, entering one every 150–250ms with slight rotation (±3°) and then a slow drift. Caption at the bottom in serif with an italic accent word ("Really *complicated*"). Used to show overwhelm; follow with a clean, single-idea scene for contrast.

## 8. Fan-out cascade
One icon tile at top; arrows draw down to 3–4 tiles (factory, bank, building, home); quote pills appear under each ("Machines will think"). A clock-style pill at top gives the timeframe ("in the next 5 to 10 years").

## 9. Metaphor visuals
Pick one that matches the idea, drawn in line style with one accent element.
- **Iceberg:** water line across the middle; small tip above, large body below; labels split above/below.
- **Funnel:** outlined funnel, dots falling in, a "compute" pill on it.
- **Gauge:** semicircle dial with a needle sweeping to a value.
- **Curve overtakes line:** dashed "Theory" line, accent "Technology" curve rises and crosses it; a "caught up" pill appears at the crossing with a dot marker.
- **Scribble:** one tangled white line drawn over 2s with a label ("Looks really complicated"); contrast with a clean version.
- **Palette-break scene (max one):** icy blue wash, falling snowflakes, centered pill.

## 10. Slider and counter
Track with a green filled portion and a round handle; label above ("Knows very little"). Handle eases from one end to the other as the narrator describes the range. Icon tiles above show the stage (sprout, etc.). Big stat card: number in serif at 7cqw with a small sans label.

## 11. Search bar
Rounded dark bar with a magnifier icon; text types one character at a time (~60ms each) with a caret. Row of person icons above, each with a small "?" badge, lighting up one at a time to show different people asking.

## 12. Speaker inset
Portrait tile pinned to the right edge (~9cqw wide) while a graphic occupies the left/center. Cut to full-frame talking head between chapters. Scene content shifts left by the inset width so nothing overlaps.

## 13. Chapter timeline
Persistent bottom timeline (see design-tokens). Hold on the new node for ~0.8s when a chapter changes, then fill the line forward. Ends the video as a "broad overview" row of year tiles, all lit equally.

## 14. Resource list
Glass card titled "Description" or "Fantastic resources" with link rows (link icon + title). Each row fades in one by one; the video thumbnail card appears beside it with a slow zoom.

## 15. Closing overview
Row of small year tiles with their labels ("1950s Perceptron … 2024 Reasoning") dimmed, then lit one by one or all together under an eyebrow ("A REALLY BROAD OVERVIEW"); finish on a serif closer with an italic accent word.

## Pacing recipes

- **Hook (0–30s):** Statement → pills (stack of 3 ideas) → quote card with portrait → search bar → metaphor. Rapid, a new visual every 4s.
- **Chapter (≈45–60s):** Statement title → timeline node change → source screenshot → live diagram → pill aside → compare or metaphor.
- **Outro:** Resource list → overview row → serif closer.

## Storyboard template

```
Beat 1 (0:00–0:05)  Scene: Statement
  Text: "Seven years"  | accent: none (eyebrow only)
  Reveals: eyebrow @0.2s, title @0.5s, 3 icon tiles @1.2s
Beat 2 (0:05–0:10)  Scene: Source screenshot
  Text: "How Many People Have Ever Lived on Earth?"  | accent: underline on the key sentence
  Reveals: frame @0.2s, underline @spoken "7%", stat card @3s
```
