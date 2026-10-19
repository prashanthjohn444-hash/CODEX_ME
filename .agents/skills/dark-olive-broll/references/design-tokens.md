# Design tokens

Contents: Color · Typography · Surfaces · Motion · Timeline · Remotion snippets · After Effects spec

## Color

| Token | Value | Use |
|---|---|---|
| `--bg` | `#161911` | Center of frame |
| `--bg-edge` | `#0f0f0c` | Vignette edge (radial gradient, ellipse at 50% 45%, ends at ~85%) |
| `--accent` | `#789858` | The only accent (sampled range `#708850`–`#789858`) |
| `--accent-soft` | `rgba(120,152,88,.18)` | Glow fill, selected tile fill |
| `--text` | `#f1efe6` | Primary text (warm off-white) |
| `--dim` | `rgba(241,239,230,.38)` | Inactive text, captions |
| `--card` | `rgba(255,255,255,.055)` | Card fill (gradient to ~.025 diagonally) |
| `--line` | `rgba(255,255,255,.12)` | 1px borders, timeline rail |
| `--pill-bg` | `#0c0d09` | Pill and code-chip fill |
| `--bad` | `#b24a3f` | Only for ✕ / "wrong" markers |
| Exception | icy teal-blue wash + white snowflakes | One allowed palette break (e.g. "winter") |

## Typography

- **Statement serif:** Instrument Serif (fallback Newsreader, Georgia). Regular weight, tight line-height ~1.05. Sizes: hero 7cqw (≈ 130px at 1080p), subhead 3.2cqw, quote 3.2cqw/1.3.
- **Key word:** same serif, *italic*, `--accent`. One per headline.
- **UI sans:** Manrope (fallback Inter, system-ui). Weight 500 for pills and labels, 600 for the active timeline label. Pill size ~1.7cqw.
- **Eyebrow:** sans, ~1.2cqw, uppercase, letter-spacing .12em, `--dim`. Orientation only.
- **Mono:** only for code/terminal (`program.py`, `> run the business while I sleep_`).
- Use container-query units (`cqw`) on a 16:9 stage so everything scales with the frame.

## Surfaces

- **Glass card:** radius 1.4cqw (~14–16px at 1080p), `linear-gradient(160deg, rgba(255,255,255,.07), rgba(255,255,255,.025))`, 1px `--line` border, shadow `0 1.6cqw 5cqw rgba(0,0,0,.4)`.
- **Active card:** border `--accent`, extra glow `0 0 3cqw --accent-soft`.
- **Pill:** inline-flex, radius 1cqw, padding .7cqw 1.4cqw, fill `--pill-bg`, 1px border, small shadow, optional leading icon or dot in accent.
- **Icon tile:** 5–6cqw rounded square, card fill, thin-stroke (≈1.5px) line icon in accent (Lucide or Phosphor).
- **Browser frame (source card):** light page screenshot inside a thin dark chrome bar with three dots; radius ~8px; caption `● SOURCE · Publisher, date` in 1.2cqw `--dim` above or below.
- **Speaker inset:** portrait crop, radius ~10px, ~9cqw wide, pinned at the right edge.

## Motion

| Property | Value |
|---|---|
| Easing (default) | `cubic-bezier(.22, 1, .36, 1)` (ease-out expo-like) |
| Entrance | opacity 0→1, translateY 1.6cqw→0, scale .98→1, blur .6cqw→0 |
| Duration | 600ms (cards 600–800ms, line draws 900ms, timeline fill 1000ms) |
| Stagger | 100–200ms between siblings; 1 reveal per spoken beat |
| Exit | 250–350ms fade + slight shrink, then next scene occupies the same positions |
| Emphasis | Border glow to accent, underline draw-on (`background-size 0→100%`, 900ms), dim others to .35 |
| Line draw | SVG `pathLength=1`, `stroke-dashoffset 1→0` |
| Camera | Slow scale 1.0→1.06 over scene length on screenshots; floating pills drift ±0.5cqw |
| Scene length | 4–8s typical; statement titles 3–4s |

Honor `prefers-reduced-motion` by removing transitions and showing the final state.

## Timeline (progress bar)

Thin rail across the bottom (left/right 6%, bottom 6%). Nodes are 1.1cqw dots with labels beneath (two lines: year, name). States: `done` = accent dot, `current` = accent dot scaled 1.5 with glow and full-white semibold label, `future` = dark dot with `--dim` label. A 2px accent line fills from the left to the current node. Keep it on screen across every scene in a chronological section; fade it out for non-sequential sections.

## Remotion snippets

```tsx
import {interpolate, useCurrentFrame, useVideoConfig, Easing} from 'remotion';

export const useReveal = (startSec: number, durSec = 0.6) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = interpolate(frame, [startSec*fps, (startSec+durSec)*fps], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.bezier(0.22, 1, 0.36, 1),
  });
  return {
    opacity: p,
    transform: `translateY(${(1 - p) * 24}px) scale(${0.98 + 0.02 * p})`,
    filter: `blur(${(1 - p) * 8}px)`,
  };
};
```

Stage: 1920×1080, 30fps, background `radial-gradient(ellipse at 50% 45%, #161911 0%, #0f0f0c 85%)`. Load fonts with `@remotion/google-fonts` (Instrument Serif, Manrope).

## After Effects / Premiere / CapCut spec

- Comp 1920×1080, 30fps, solid background `#161911` with a radial vignette adjustment layer to `#0f0f0c`.
- Entrances: Position Y +24px → 0, Opacity 0 → 100, Scale 98 → 100, Gaussian Blur 8 → 0; keyframe ease: Easy Ease Out with influence ~85% (approximates the expo curve), 18 frames.
- Stagger layers by 3–6 frames. Stroke draws via Trim Paths 0 → 100%.
- Text: Instrument Serif for statements (italic accent for key word), Manrope Medium for pills.
