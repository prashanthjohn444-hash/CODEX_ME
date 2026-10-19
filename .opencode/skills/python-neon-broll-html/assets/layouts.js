/* Shared layout builder: returns the scene markup for a SCENE config. Used by the HTML player and the HyperFrames export. */
function buildHTML(S){
 const ver=S._ver||{},strip=s=>String(s).replace(/<[^>]+>/g,'');
 /* V: a value element; when the scene changes it with set:, every version is pre-rendered so the timeline can cross-fade (seek-safe) */
 const V=(tag,id,cls,text,wide)=>{const vs=ver[id];if(!vs)return `<${tag} class="${cls}" id="${id}">${text}</${tag}>`;
  const st=wide?` style="min-width:${Math.max(...vs.map(v=>strip(v).length))}ch"`:'';
  return `<${tag} class="${cls} has-ver" id="${id}"${st}>`+vs.map((v,k)=>`<span class="ver${k?' o':''}" id="${id}_${k}">${v}</span>`).join('')+`</${tag}>`};
 const code=(a,p)=>a.map((l,i)=>`<div class="code ln" id="${p}${i}">${l}</div>`).join('');
 const outp=a=>a.map((l,i)=>`<div class="res ln" id="o${i}">${l}</div>`).join('');
 const P=(cls,id,t,body,st='')=>`<div class="panel ${cls} fade" id="${id}" style="${st}"><div class="t">${t}</div>${body}</div>`;
 const cellsH=cs=>`<div class="cells">${cs.map((c,i)=>`<div class="cell" id="c${i}">${V('div','c'+i+'v','b',c[0])}<div class="i">${c[1]}</div></div>`).join('')}</div>`;
 const badges=(S.badges||[]).length?`<span class="badges">${S.badges.join('')}</span>`:'';
 const H=`<h1 class="fade" id="h">${S.title}<small>${S.subtitle}</small>${badges}</h1>`;
const NODES=back=>{const n=S.nodes.length,cols=Array(n).fill('1fr').join(' auto ');
  return `<div class="fade" id="nodes"><div class="nodes" style="grid-template-columns:${cols}">`+S.nodes.map((nd,i)=>(i?`<span class="ar">→</span>`:'')+`<div class="node" id="n${i}"><div class="nl">${nd[0]}</div>${V('div','n'+i+'v','v',nd[1])}</div>`).join('')+(back&&n>2?`<div class="back" style="grid-column:3/${2*n}"></div>`:'')+`</div></div>`};
 const LAY={
  lanes:()=>H+P('pin','pin',S.input.label,code(S.input.lines,'l'))+P('pmem','pmem',S.memory.label,cellsH(S.memory.cells))+P('pout','pout',S.output.label,outp(S.output.lines)),
  decision:()=>H+`<div class="row">`+P('pin','pin',S.input.label,code(S.input.lines,'l'),'width:38%')+`<div class="col">`+
   P('pmem','cond',S.cond.label||'CONDITION',`<div class="big">${S.cond.text} → ${V('span','cv','v',S.cond.start||'?',1)}</div>`)+
   `<div class="branches">`+P('pbt','bt','TRUE',S.branches.t.map(l=>`<div class="code">${l}</div>`).join(''))+P('pbf','bf','FALSE',S.branches.f.map(l=>`<div class="code">${l}</div>`).join(''))+`</div></div></div>`+
   P('pout','pout',S.output.label,outp(S.output.lines)),
  loop:()=>H+`<div class="row">`+P('pin','pin',S.input.label,code(S.input.lines,'l'),'width:34%')+`<div class="col">`+NODES(true)+
   cellsH([[S.counter.value,S.counter.name]])+`</div></div>`+P('pout','pout',S.output.label,outp(S.output.lines)),
  flow:()=>H+P('pin','pin',S.input.label,code(S.input.lines,'l'))+NODES(false)+P('pout','pout',S.output.label,outp(S.output.lines)),
  compare:()=>H+(S.input?P('pin','pin',S.input.label,code(S.input.lines,'l')):'')+`<div class="branches">`+P('pbt','bt',S.left.label,code(S.left.lines,'a'))+P('pbf','bf',S.right.label,code(S.right.lines,'b'))+`</div>`+(S.output?P('pout','pout',S.output.label,outp(S.output.lines)):'')
 };
 return LAY[S.layout||'lanes']();
}
if(typeof module!=='undefined')module.exports={buildHTML};
