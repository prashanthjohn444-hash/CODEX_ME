/* Pure timeline: the state at time t is every step with time <= t applied in order. No hooks, no timers. */
export type Step = [number, string];
export interface State {
  show: Record<string, number>; // id -> time it was shown
  hot: Record<number, number>; // cell index -> 0..1 glow
  lit: Record<string, number>; // id -> 0..1 glow
  dim: Record<string, number>; // id -> time it was dimmed
  text: Record<string, string>; // id -> replaced text (set:)
}
const clamp = (x: number) => Math.min(1, Math.max(0, x));
export const prog = (start: number | undefined, t: number, d: number) => (start === undefined ? 0 : clamp((t - start) / d));
export const easeOut = (p: number) => 1 - Math.pow(1 - p, 3);
export const easeBack = (p: number) => 1 + 2.4 * Math.pow(p - 1, 3) + 1.4 * Math.pow(p - 1, 2);

export function stateAt(steps: Step[], t: number, glowSecs = 0.4): State {
  const show: State['show'] = {}, dim: State['dim'] = {}, text: State['text'] = {};
  const hotEv: Record<number, [number, boolean]> = {}, litEv: Record<string, [number, boolean]> = {};
  let hot = new Set<number>(), lit = new Set<string>();
  for (const [ts, c] of [...steps].sort((a, b) => a[0] - b[0])) {
    if (ts > t) break;
    const i = c.indexOf(':'), k = c.slice(0, i), v = c.slice(i + 1);
    if (k === 'show') v.split(',').forEach((id) => (show[id] = ts));
    else if (k === 'dim') v.split(',').forEach((id) => (dim[id] = ts));
    else if (k === 'hot') {
      const n = new Set<number>(v ? v.split(',').map(Number) : []);
      hot.forEach((x) => { if (!n.has(x)) hotEv[x] = [ts, false]; });
      n.forEach((x) => { if (!hot.has(x)) hotEv[x] = [ts, true]; });
      hot = n;
    } else if (k === 'lit') {
      const n = new Set<string>(v ? v.split(',') : []);
      lit.forEach((x) => { if (!n.has(x)) litEv[x] = [ts, false]; });
      n.forEach((x) => { if (!lit.has(x)) litEv[x] = [ts, true]; });
      lit = n;
    } else if (k === 'set') {
      const j = v.indexOf('=');
      text[v.slice(0, j)] = v.slice(j + 1);
    }
  }
  const glow = (e: [number, boolean]) => (e[1] ? clamp((t - e[0]) / glowSecs) : 1 - clamp((t - e[0]) / glowSecs));
  const hotP: State['hot'] = {}, litP: State['lit'] = {};
  Object.entries(hotEv).forEach(([x, e]) => (hotP[+x] = glow(e)));
  Object.entries(litEv).forEach(([x, e]) => (litP[x] = glow(e)));
  return {show, hot: hotP, lit: litP, dim, text};
}
