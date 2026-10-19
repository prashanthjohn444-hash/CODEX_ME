import { mkdir, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import ffmpeg from '../node_modules/ffmpeg-static/index.js';
import ffprobe from '../node_modules/ffprobe-static/index.js';
import { scenes } from './scenes.mjs';

const base = path.resolve('premium-white');
const bin = path.resolve('node_modules/.bin/hyperframes.cmd');
const browser = path.join(process.env.USERPROFILE || '', '.cache', 'hyperframes', 'chrome', 'chrome-headless-shell', 'win64-152.0.7977.30', 'chrome-headless-shell-win64', 'chrome-headless-shell.exe');
const env = { ...process.env, FFMPEG_PATH: ffmpeg, FFPROBE_PATH: ffprobe.path,
  HYPERFRAMES_BROWSER_PATH: browser, HYPERFRAMES_NO_UPDATE_CHECK: '1',
  PATH: [path.dirname(ffmpeg), path.dirname(ffprobe.path), process.env.PATH].join(path.delimiter) };

function html(s) {
  const beats = s.beats.map((t, i) => `tl.fromTo(reveals[${i}],{opacity:0,y:17},{opacity:1,y:0,duration:.62,ease:'power2.out'},${t});`).join('\n');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1920"><title>${s.title}</title><link rel="stylesheet" href="style.css"><script src="assets/gsap.min.js"></script></head><body>
<main id="root" data-composition-id="root" data-start="0" data-duration="${s.duration}" data-width="1920" data-height="1080" data-fps="30">
<div class="stage"><div class="hf-dynamic-grid" data-layout-ignore aria-hidden="true"></div><div class="wash" data-layout-ignore></div>
<div class="content"><div class="kicker"><div class="brand"><span class="brand-mark"></span>PYTHON / DAY 01</div><div class="meta">TECHNICAL FIELD NOTE · ${s.id.slice(0,2)}</div></div>
<header class="header"><h1>${s.title}</h1><div class="deck">${s.deck}</div><div class="header-rule"></div></header>
<section class="canvas">${s.body}</section></div>
<div class="stage-meta"><span>PYTHON FOUNDATIONS</span><span>01 / READ • TEST • REPEAT</span></div></div></main>
<script>const tl=gsap.timeline({paused:true});const reveals=Array.from(document.querySelectorAll('.reveal'));
tl.fromTo('.header',{opacity:0,y:12},{opacity:1,y:0,duration:.58,ease:'power2.out'},0);
tl.fromTo('.header-rule',{scaleX:0},{scaleX:1,duration:.78,ease:'power3.out'},.18);
${beats}
tl.fromTo('.hf-dynamic-grid',{'--hf-grid-x':'0px','--hf-grid-y':'0px'},{'--hf-grid-x':'28px','--hf-grid-y':'-14px',duration:${s.duration},ease:'none'},0);
window.__timelines=window.__timelines||{};window.__timelines.root=tl;</script></body></html>`;
}

await mkdir(path.join(base, 'renders'), {recursive:true});
const manifest = { format:'day-01-premium-white-broll/v1', width:1920, height:1080, fps:30,
  audio:false, background:'warm white with fine technical grid', source:'HyperFrames, diagrams not screen recordings', clips:[] };
for (const s of scenes.filter(x => process.argv.length <= 2 || process.argv.slice(2).includes(x.id))) {
  await writeFile(path.join(base, 'source', `${s.id}.html`), html(s), 'utf8');
  await writeFile(path.join(base, 'index.html'), html(s), 'utf8');
  const check=spawnSync(bin,['check','premium-white','--json'],{cwd:path.resolve('.'),env,encoding:'utf8',shell:true,timeout:120000});
  if(check.status !== 0) throw Error(`HyperFrames check failed ${s.id}: ${check.stdout || check.stderr}`);
  const output = `premium-white/renders/${s.id}.mp4`;
  const render = spawnSync(bin,['render','-c','premium-white/index.html','-o',output,'--fps','30','--workers','1','--quality','high'],
    {cwd:path.resolve('.'),env,encoding:'utf8',shell:true,timeout:600000});
  if (render.status !== 0) throw Error(`HyperFrames failed ${s.id}: ${render.error || render.status}`);
  const probe = spawnSync(ffprobe.path,['-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames,duration','-of','json',path.resolve(output)],{encoding:'utf8'});
  if(probe.status !== 0) throw Error(`Probe failed ${s.id}: ${probe.stderr}`);
  const stream=JSON.parse(probe.stdout).streams[0];
  if(stream.width!==1920||stream.height!==1080||stream.r_frame_rate!=='30/1') throw Error(`Invalid render ${s.id}`);
  manifest.clips.push({id:s.id,file:`renders/${s.id}.mp4`,source:`source/${s.id}.html`,frames:Number(stream.nb_frames),duration_seconds:Number(stream.duration),beats:s.beats});
  await writeFile(path.join(base,'manifest.json'),JSON.stringify(manifest,null,2),'utf8');
  console.log(`Verified ${s.id}: ${stream.nb_frames} frames`);
}
