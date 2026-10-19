#!/usr/bin/env node
/* node build.js <scene.js> <outDir> [--target html|hyperframes|remotion|all]   (default: html)
   scene.js: `const SCENE={...};`  theme: neon|paper|terminal · layout: lanes|decision|loop|flow|compare
   {{logo:python}} in any text, or logo:"python" / logos:[...] for heading badges. Default length 4.5 s (+0.4 s hold). */
const fs=require('fs'),path=require('path'),vm=require('vm');
const ROOT=path.join(__dirname,'..'),A=path.join(ROOT,'assets'),logos=require('./logos.js'),{themes,cssVars}=require('../assets/themes.js'),{buildHTML}=require('../assets/layouts.js');
const argv=process.argv.slice(2),ti=argv.indexOf('--target'),TARGET=ti>=0?argv[ti+1]:'html',pos=argv.filter((a,i)=>!a.startsWith('--')&&argv[i-1]!=='--target');
const [scenePath,outDir]=pos;
if(!scenePath||!outDir){console.error('usage: node build.js scene.js outDir [--target html|hyperframes|remotion|all]');process.exit(1)}
let S=vm.runInNewContext(fs.readFileSync(scenePath,'utf8')+';SCENE');
const name=path.basename(scenePath,'.js'),FPS=30,warns=[],W=m=>{warns.push(m);console.warn('! '+name+': '+m)};
const P=themes[S.theme||'neon']||(W(`unknown theme "${S.theme}", using neon`),themes.neon);S.theme=S.theme||'neon';
const noLogo=k=>W(`no logo for "${k}" (not in simple-icons). Put the official SVG at assets/logos/custom/<slug>.svg or leave it out; no look-alike is drawn.`);
const expand=s=>s.replace(/\{\{logo:([^}]+)\}\}/g,(m,k)=>{const l=logos.resolve(k);if(!l){noLogo(k);return''}return logos.svgFor(l,'logo',P.dark)});
const walk=v=>typeof v==='string'?expand(v):Array.isArray(v)?v.map(walk):v&&typeof v==='object'?Object.fromEntries(Object.entries(v).map(([a,b])=>[a,walk(b)])):v;
const keys=[].concat(S.logo||[],S.logos||[]);
S=walk(S);S.badges=keys.map(k=>{const l=logos.resolve(k);if(!l){noLogo(k);return null}return logos.svgFor(l,'logo',P.dark)}).filter(Boolean);delete S.logo;delete S.logos;
const DUR=S.duration||4.5,HOLD=S.hold??0.4;S.duration=DUR;S.hold=HOLD;S.palette=P;

/* ---- lint: short, readable, ids that exist ---- */
const plain=s=>String(s).replace(/<[^>]+>/g,'');
if(DUR+HOLD>5.2)W(`${(DUR+HOLD).toFixed(1)} s is over the 5 s target for course B-roll`);
const lineSets={input:S.input&&S.input.lines,left:S.left&&S.left.lines,right:S.right&&S.right.lines,output:S.output&&S.output.lines};
for(const [k,v] of Object.entries(lineSets)){const max=k==='input'?({decision:5,loop:4}[S.layout]||3):3;if(v&&v.length>max)W(`${k} has ${v.length} lines; keep to ${max} or fewer for a clip this short`)}
for(const [k,v] of Object.entries(lineSets))(v||[]).forEach(l=>{if(plain(l).length>42)W(`${k} line is long ("${plain(l).slice(0,24)}…"): shorten for phones`)});
if(plain(S.title||'').length>22)W('title is long; 22 characters or fewer reads best');
if(plain(S.subtitle||'').length>60)W('subtitle is long; 60 characters or fewer');
const ids=new Set([...buildHTML(S).matchAll(/ id="([^"]+)"/g)].map(m=>m[1]));
const valId=id=>id==='cv'?'cv':/^[cn]\d+$/.test(id)?id+'v':id;
S.steps.forEach(([t,c])=>{const i=c.indexOf(':'),k=c.slice(0,i),v=c.slice(i+1);
 if(t>DUR)W(`step "${c}" at ${t}s is after the scene duration ${DUR}s`);
 if(k==='show'||k==='dim'||k==='lit')v.split(',').filter(Boolean).forEach(id=>{if(!ids.has(id))W(`step "${c}": id "${id}" does not exist in layout "${S.layout}"`)});
 else if(k==='hot')v.split(',').filter(Boolean).forEach(n=>{if(!ids.has('c'+n))W(`step "${c}": cell ${n} does not exist`)});
 else if(k==='set'){const id=v.slice(0,v.indexOf('='));if(!ids.has(valId(id)))W(`step "${c}": nothing to set at "${id}"`)}
 else W(`unknown step command "${k}"`)});

const layouts=fs.readFileSync(path.join(A,'layouts.js'),'utf8'),tpl=fs.readFileSync(path.join(A,'template.html'),'utf8');
fs.mkdirSync(outDir,{recursive:true});
const wr=(p,c)=>{fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,c);console.log('wrote',p)};

function html(){
 const out=tpl.replace(/\/\*SCENE\*\/[\s\S]*?\/\*END_SCENE\*\//,()=>'/*SCENE*/\nconst SCENE='+JSON.stringify(S)+';\n/*END_SCENE*/')
  .replace(/\/\*LAYOUTS\*\/[\s\S]*?\/\*END_LAYOUTS\*\//,()=>'/*LAYOUTS*/\n'+layouts+'/*END_LAYOUTS*/')
  .replace(/\/\*THEME\*\/[\s\S]*?\/\*END_THEME\*\//,()=>cssVars(P));
 wr(path.join(outDir,name+'-broll.html'),out)}

/* ---------- HyperFrames: one paused GSAP timeline registered as window.__timelines.main ---------- */
function origText(id){let m;if((m=id.match(/^c(\d+)$/)))return S.memory?S.memory.cells[+m[1]][0]:S.counter.value;if((m=id.match(/^n(\d+)$/)))return S.nodes[+m[1]][1];if(id==='cv')return S.cond.start||'?';return''}
function hyperframes(){
 const steps=[...S.steps].sort((a,b)=>a[0]-b[0]),ver={};
 steps.forEach(([t,c])=>{if(c.startsWith('set:')){const v=c.slice(4),j=v.indexOf('='),id=v.slice(0,j),vid=valId(id);(ver[vid]=ver[vid]||[origText(id)]).push(v.slice(j+1))}});
 const body=buildHTML({...S,_ver:ver}),sh=(rgb,a,b,c)=>`0 0 ${b}px ${c}px rgba(${rgb},${a})`;
 const css=cssVars(P)+tpl.match(/<style>([\s\S]*?)<\/style>/)[1].replace(/\/\*THEME\*\/[\s\S]*?\/\*END_THEME\*\//,'').replace(/^:root\{[^\n]*\}$/m,'')+`
/* --- HyperFrames overrides: seek-based rendering, no CSS transitions; GSAP owns every change --- */
html,body{width:1920px;height:1080px;overflow:hidden;background:${P.bg};display:block;padding:0;margin:0}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:${P.bg}}
.clip{position:absolute;inset:0}.scale{max-width:none;width:1920px;height:1080px}
*,*::before{transition:none!important;animation:none!important}
.ln{height:3.2cqw}.cell .b,.node{box-shadow:${sh(P.vr,0,0,0)}}
.panel.pin,.panel.pbt{box-shadow:${sh(P.gr,P.sp,38,-12)}}.panel.pmem{box-shadow:${sh(P.vr,P.sp,38,-12)}}.panel.pout,.panel.pbf{box-shadow:${sh(P.cr,P.sp,38,-12)}}`;
 const L=[],ga=P.ga;
 const ON={cell:{backgroundColor:`rgba(${P.vr},${P.dark?.38:.18})`,borderColor:P.v,boxShadow:sh(P.vr,ga,42,0)},node:{backgroundColor:`rgba(${P.vr},${P.dark?.35:.16})`,borderColor:P.v,boxShadow:sh(P.vr,ga,46,0)}};
 const OFF={cell:{backgroundColor:`rgba(${P.vr},.08)`,borderColor:`rgba(${P.vr},.6)`,boxShadow:sh(P.vr,0,0,0)},node:{backgroundColor:`rgba(${P.vr},0)`,borderColor:`rgba(${P.vr},.55)`,boxShadow:sh(P.vr,0,0,0)}};
 const RGB={bt:P.gr,bf:P.cr,pin:P.gr,pout:P.cr,cond:P.vr,pmem:P.vr};
 const to=(sel,o,t,d)=>L.push(`tl.to(${JSON.stringify(sel)},${JSON.stringify({...o,duration:d,ease:'power2.out'})},${t});`);
 let hot=new Set(),lit=null;const seqN={};
 const setLit=(id,on,t)=>{if(/^n\d$/.test(id))to('#'+id,on?ON.node:OFF.node,t,.4);else to('#'+id,on?{boxShadow:sh(RGB[id]||P.cr,ga,58,0),backgroundColor:P.pfl}:{boxShadow:sh(RGB[id]||P.cr,P.sp,38,-12),backgroundColor:P.pf},t,.4)};
 for(const [t,c] of steps){const i=c.indexOf(':'),k=c.slice(0,i),v=c.slice(i+1);
  if(k==='show')v.split(',').filter(Boolean).forEach(id=>{
   if(/^[laob]\d+$/.test(id))to('#'+id,{opacity:1},t,.4);
   else if(/^c\d+$/.test(id))L.push(`tl.to("#${id}",{opacity:1,scale:1,duration:.45,ease:"back.out(1.4)"},${t});`);
   else to('#'+id,{opacity:1,y:0},t,.6)});
  else if(k==='hot'){const n=new Set(v?v.split(',').map(Number):[]);
   hot.forEach(x=>{if(!n.has(x)){to(`#c${x}v`,OFF.cell,t,.4);to(`#c${x} .i`,{color:P.idx},t,.4)}});
   n.forEach(x=>{if(!hot.has(x)){to(`#c${x}v`,ON.cell,t,.4);to(`#c${x} .i`,{color:P.hd},t,.4)}});hot=n}
  else if(k==='lit'){if(lit)lit.forEach(id=>setLit(id,false,t));lit=v?v.split(','):null;if(lit)lit.forEach(id=>setLit(id,true,t))}
  else if(k==='dim')v.split(',').forEach(id=>to('#'+id,{opacity:.25},t,.4));
  else if(k==='set'){const vid=valId(v.slice(0,v.indexOf('=')));const n=(seqN[vid]=(seqN[vid]||0)+1);L.push(`tl.set("#${vid}_${n-1}",{opacity:0},${t});tl.set("#${vid}_${n}",{opacity:1},${t});`)}}
 const D=+(DUR+HOLD).toFixed(2);
 wr(path.join(outDir,'hyperframes','index.html'),`<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>${css}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="${D}" data-width="1920" data-height="1080" data-fps="${FPS}">
 <section id="scene-clip" class="clip" data-start="0" data-duration="${D}" data-track-index="0"><div class="scale"><div class="scene" id="scene">${body}</div></div></section>
</div>
<script>
window.__timelines=window.__timelines||{};
const tl=gsap.timeline({paused:true});
${L.join('\n')}
tl.to({},{duration:.01},${(D-.01).toFixed(2)}); /* pins the timeline length to the composition */
window.__timelines.main=tl;
</script></body></html>
`)}

function remotion(){
 const src=path.join(A,'remotion'),copy=(s,d)=>{for(const f of fs.readdirSync(s)){const sp=path.join(s,f),dp=path.join(d,f);fs.statSync(sp).isDirectory()?copy(sp,dp):wr(dp,fs.readFileSync(sp))}};
 copy(src,path.join(outDir,'remotion'));
 wr(path.join(outDir,'remotion','src','scene.json'),JSON.stringify({...S,fps:FPS},null,1))}

if(TARGET==='html'||TARGET==='all')html();
if(TARGET==='hyperframes'||TARGET==='all')hyperframes();
if(TARGET==='remotion'||TARGET==='all')remotion();
if(warns.length)process.exitCode=0;
