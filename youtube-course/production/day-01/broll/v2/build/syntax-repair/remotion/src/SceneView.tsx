import React from 'react';
import {stateAt, prog, easeOut, easeBack} from './timeline';

const U = 19.2; // 1cqw at 1920px, so sizes match the HTML player
const MONO = 'ui-monospace,Menlo,Consolas,monospace';
const hex = (h: string) => [1, 3, 5].map((i) => parseInt(h.substr(i, 2), 16));
const mix = (a: string, b: string, p: number) => { const x = hex(a), y = hex(b); return `rgb(${x.map((v, i) => Math.round(v + (y[i] - v) * p)).join(',')})`; };

const Html: React.FC<{h: string; style?: React.CSSProperties}> = ({h, style}) => <span style={style} dangerouslySetInnerHTML={{__html: h}} />;

export const SceneView: React.FC<{scene: any; t: number}> = ({scene: S, t}) => {
  const P = S.palette; // colours come from the scene's theme (neon | paper | terminal)
  const HEAD = P.head || "'Bebas Neue','Noto Sans Telugu','Oswald','Arial Narrow',Impact,sans-serif";
  const BODY = "'Barlow','Noto Sans Telugu','Segoe UI',system-ui,sans-serif";
  const st = stateAt(S.steps, t);
  const shown = (id: string, d = 0.6) => easeOut(prog(st.show[id], t, d));
  const dimF = (id: string) => (st.dim[id] === undefined ? 1 : 1 - 0.75 * easeOut(prog(st.dim[id], t, 0.4)));
  const text = (id: string, orig: string) => st.text[id] ?? orig;
  const css = `.logo{width:1.1em;height:1.1em;vertical-align:-.14em;flex:none}
.badges .logo{width:${4.4 * U}px;height:${4.4 * U}px}.cellb .logo{width:${3.6 * U}px;height:${3.6 * U}px}
.res em{font-style:normal;color:${P.mut2};font-size:${1.8 * U}px}
.res strong{color:${P.c};font-weight:600;text-shadow:0 0 ${1.4 * U}px rgba(${P.cr},${P.ga});font-size:${3 * U}px}`;

  const Panel: React.FC<{id: string; k: string; rgb: string; title: string; style?: React.CSSProperties; children?: React.ReactNode}> = ({id, k, rgb, title, style, children}) => {
    const p = shown(id), g = st.lit[id] || 0;
    return (
      <div style={{position: 'relative', border: `1px solid ${k}`, borderRadius: 1.4 * U, padding: `${1.2 * U}px ${2 * U}px`, background: P.pf,
        boxShadow: `0 0 ${38 + 20 * g}px ${-12 * (1 - g)}px rgba(${rgb},${P.sp + (P.ga - P.sp) * g})`, opacity: p * dimF(id), transform: `translateY(${(1 - p) * U}px)`, ...style}}>
        <div style={{position: 'absolute', inset: 0, borderRadius: 'inherit', background: P.pfl, opacity: g, pointerEvents: 'none'}} />
        <div style={{position: 'relative', fontFamily: HEAD, fontSize: 2.2 * U, color: k, letterSpacing: '.06em', marginBottom: 0.5 * U}}>{title}</div>
        <div style={{position: 'relative'}}>{children}</div>
      </div>
    );
  };
  const Line: React.FC<{id: string; h: string; res?: boolean}> = ({id, h, res}) => (
    <div className={res ? 'res' : undefined} style={{height: 3.2 * U, overflow: 'hidden', opacity: shown(id, 0.4), fontFamily: MONO, fontSize: (res ? 2.4 : 2.1) * U,
      color: res ? P.res : P.ink, lineHeight: 1.5, display: res ? 'flex' : 'block', gap: 1.6 * U, alignItems: 'baseline'}}>
      <Html h={h} />
    </div>
  );
  const Lines: React.FC<{prefix: string; lines: string[]; res?: boolean}> = ({prefix, lines, res}) => <>{lines.map((l, i) => <Line key={i} id={prefix + i} h={l} res={res} />)}</>;
  const Cells: React.FC<{cells: [string, string | number][]}> = ({cells}) => (
    <div style={{display: 'flex', gap: 1.4 * U, justifyContent: 'center', alignItems: 'flex-start', marginTop: 0.4 * U}}>
      {cells.map(([main, idx], i) => {
        const id = 'c' + i, p = prog(st.show[id], t, 0.45), h = st.hot[i] || 0;
        return (
          <div key={id} style={{width: 7.2 * U, textAlign: 'center', opacity: easeOut(p), transform: `scale(${0.6 + 0.4 * easeBack(p)})`}}>
            <div className="cellb" style={{height: 6 * U, borderRadius: U, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: MONO, fontSize: 3.6 * U, color: P.hd,
              border: `1.5px solid rgba(${P.vr},${0.6 + 0.4 * h})`, background: `rgba(${P.vr},${0.08 + (P.dark ? 0.3 : 0.1) * h})`, boxShadow: `0 0 ${2.2 * U * h}px rgba(${P.vr},${P.ga * h})`}}>
              <Html h={text(id, String(main))} />
            </div>
            <div style={{fontFamily: MONO, fontSize: 1.7 * U, marginTop: 0.5 * U, color: mix(P.idx, P.hd, h)}}>{idx}</div>
          </div>
        );
      })}
    </div>
  );
  const Heading = () => {
    const p = shown('h');
    return (
      <div style={{display: 'flex', alignItems: 'center', fontFamily: HEAD, fontSize: 5.2 * U, color: P.hd, letterSpacing: '.02em', lineHeight: 1, opacity: p, transform: `translateY(${(1 - p) * U}px)`}}>
        <Html h={S.title} />
        <span style={{fontFamily: BODY, fontSize: 1.6 * U, color: P.mut, marginLeft: 1.6 * U, letterSpacing: 0}}><Html h={S.subtitle} /></span>
        {S.badges?.length ? <span className="badges" style={{marginLeft: 'auto', display: 'inline-flex', gap: 1.2 * U, alignItems: 'center'}}><Html h={S.badges.join('')} /></span> : null}
      </div>
    );
  };
  const Input: React.FC<{w?: string}> = ({w}) => (
    <Panel id="pin" k={P.g} rgb={P.gr} title={S.input.label} style={w ? {width: w, flex: 'none'} : {flex: 'none'}}><Lines prefix="l" lines={S.input.lines} /></Panel>
  );
  const Output = () => (
    <Panel id="pout" k={P.c} rgb={P.cr} title={S.output.label} style={{flex: 1}}><Lines prefix="o" lines={S.output.lines} res /></Panel>
  );
  const Nodes: React.FC<{back: boolean}> = ({back}) => {
    const np = shown('nodes'), n = S.nodes.length;
    return (
      <div style={{opacity: np, transform: `translateY(${(1 - np) * U}px)`}}>
        <div style={{display: 'grid', gridTemplateColumns: Array(n).fill('1fr').join(' auto '), alignItems: 'center', gap: 0.6 * U}}>
          {S.nodes.map(([label, tx]: [string, string], i: number) => {
            const l = st.lit['n' + i] || 0;
            return (
              <React.Fragment key={i}>
                {i ? <span style={{color: P.v, fontSize: 2.2 * U}}>→</span> : null}
                <div style={{borderRadius: 1.1 * U, padding: `${U}px ${0.6 * U}px`, textAlign: 'center', border: `1px solid rgba(${P.vr},${0.55 + 0.45 * l})`,
                  background: `rgba(${P.vr},${(P.dark ? 0.35 : 0.16) * l})`, boxShadow: `0 0 ${2.4 * U * l}px rgba(${P.vr},${P.ga * l})`}}>
                  <div style={{fontFamily: HEAD, fontSize: 1.9 * U, color: P.v, letterSpacing: '.06em'}}><Html h={label} /></div>
                  <div style={{fontFamily: MONO, fontSize: 2 * U, color: P.hd}}><Html h={text('n' + i, tx)} /></div>
                </div>
              </React.Fragment>
            );
          })}
          {back && n > 2 ? <div style={{gridColumn: `3 / ${2 * n}`, height: 2.2 * U, border: `2px dotted rgba(${P.vr},.7)`, borderTop: 0, borderRadius: `0 0 ${U}px ${U}px`, margin: `0 ${4 * U}px`}} /> : null}
        </div>
      </div>
    );
  };
  const Code: React.FC<{lines: string[]}> = ({lines}) => <>{lines.map((l, i) => <div key={i} style={{fontFamily: MONO, fontSize: 2.1 * U, color: P.ink, lineHeight: 1.5}}><Html h={l} /></div>)}</>;

  let body: React.ReactNode;
  if (S.layout === 'decision') {
    body = (
      <>
        <Heading />
        <div style={{display: 'flex', gap: 1.5 * U}}>
          <Input w="38%" />
          <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 1.5 * U}}>
            <Panel id="cond" k={P.v} rgb={P.vr} title={S.cond.label || 'CONDITION'}>
              <div style={{fontFamily: MONO, fontSize: 2.8 * U, color: P.hd}}>{S.cond.text} → <span style={{color: P.v, fontWeight: 600}}>{text('cv', S.cond.start || '?')}</span></div>
            </Panel>
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 1.5 * U}}>
              <Panel id="bt" k={P.g} rgb={P.gr} title="TRUE"><Code lines={S.branches.t} /></Panel>
              <Panel id="bf" k={P.c} rgb={P.cr} title="FALSE"><Code lines={S.branches.f} /></Panel>
            </div>
          </div>
        </div>
        <Output />
      </>
    );
  } else if (S.layout === 'loop') {
    body = (
      <>
        <Heading />
        <div style={{display: 'flex', gap: 1.5 * U}}>
          <Input w="34%" />
          <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 1.5 * U}}>
            <Nodes back />
            <Cells cells={[[S.counter.value, S.counter.name]]} />
          </div>
        </div>
        <Output />
      </>
    );
  } else if (S.layout === 'flow') {
    body = (<><Heading /><Input /><Nodes back={false} /><Output /></>);
  } else if (S.layout === 'compare') {
    body = (
      <>
        <Heading />
        {S.input ? <Input /> : null}
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 1.5 * U}}>
          <Panel id="bt" k={P.g} rgb={P.gr} title={S.left.label}><Lines prefix="a" lines={S.left.lines} /></Panel>
          <Panel id="bf" k={P.c} rgb={P.cr} title={S.right.label}><Lines prefix="b" lines={S.right.lines} /></Panel>
        </div>
        {S.output ? <Output /> : null}
      </>
    );
  } else {
    body = (
      <>
        <Heading />
        <Input />
        <Panel id="pmem" k={P.v} rgb={P.vr} title={S.memory.label} style={{flex: 'none'}}><Cells cells={S.memory.cells} /></Panel>
        <Output />
      </>
    );
  }
  return (
    <div style={{position: 'relative', width: 1920, height: 1080, boxSizing: 'border-box', overflow: 'hidden', background: P.bg, color: P.ink, fontFamily: BODY,
      padding: `${3.2 * U}px ${4 * U}px`, display: 'flex', flexDirection: 'column', gap: 1.5 * U,
      backgroundImage: `linear-gradient(${P.grid} 1px,transparent 1px),linear-gradient(90deg,${P.grid} 1px,transparent 1px)`, backgroundSize: `${3 * U}px ${3 * U}px`}}>
      <style>{css}</style>
      {body}
    </div>
  );
};
