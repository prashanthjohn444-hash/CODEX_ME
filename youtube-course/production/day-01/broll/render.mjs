import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import ffmpeg from 'ffmpeg-static';
import ffprobe from 'ffprobe-static';
import { scenes } from './scenes.mjs';

const root = process.cwd();
const out = path.join(root, 'renders');
const bin = path.join(root, 'node_modules', '.bin', 'hyperframes.cmd');
const browser = path.join(process.env.USERPROFILE || '', '.cache', 'hyperframes', 'chrome', 'chrome-headless-shell', 'win64-152.0.7977.30', 'chrome-headless-shell-win64', 'chrome-headless-shell.exe');
const env = {
  ...process.env,
  FFMPEG_PATH: ffmpeg,
  FFPROBE_PATH: ffprobe.path,
  HYPERFRAMES_BROWSER_PATH: browser,
  HYPERFRAMES_NO_UPDATE_CHECK: '1',
  PATH: [path.dirname(ffmpeg), path.dirname(ffprobe.path), process.env.PATH].join(path.delimiter),
};

const buildHTML = ({ id, duration, title, body }) => `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1920"><title>${title}</title><link rel="stylesheet" href="./style.css"><script src="./node_modules/gsap/dist/gsap.min.js"></script></head>
<body><main id="root" data-composition-id="root" data-start="0" data-width="1920" data-height="1080" data-fps="30">
<div class="stage"><div class="grid"></div><div class="orb"></div><div class="content"><header class="header"><div class="eyebrow"><span>PY / 30</span> DAY 01 · THE FIRST PROGRAM</div><h1>${title}</h1><div class="rule"></div></header>${body}</div><footer class="footer"><span>PYTHON FOUNDATIONS</span><span>01 / TECHNICAL NOTES</span></footer></div><div id="end-marker" hidden></div>
</main><script>
  const tl=gsap.timeline({paused:true});
  tl.fromTo('.stage',{opacity:0},{opacity:1,duration:.38,ease:'power2.inOut'},0);
  tl.fromTo('.content',{filter:'blur(10px)',opacity:.3},{filter:'blur(0px)',opacity:1,duration:.55,ease:'power2.inOut'},0);
  tl.fromTo('.content',{x:14,scale:1.012},{x:-8,scale:1,duration:${duration},ease:'sine.inOut'},0);
  tl.fromTo('.orb',{x:0,y:0},{x:-85,y:35,duration:${duration},ease:'sine.inOut'},0);
  tl.fromTo('.reveal',{opacity:0,y:22},{opacity:1,y:0,duration:.54,stagger:.15,ease:'power2.out'},.35);
  ${id === '05-syntax-repair' ? `tl.set('.step-before',{display:'none'},1.78);tl.set('.step-after',{display:(i,el)=>el.classList.contains('success-line')?'block':'inline',opacity:0},1.78);tl.to('.step-after',{opacity:1,duration:.22,ease:'steps(3)'},1.78);` : ''}
  tl.to('.content',{filter:'blur(7px)',opacity:0,duration:.3,ease:'power2.inOut'},${duration - .3});
  tl.to('.stage',{opacity:0,duration:.26,ease:'power2.inOut'},${duration - .26});
  tl.set('#end-marker',{opacity:1},${duration});
  window.__timelines=window.__timelines||{};window.__timelines.root=tl;
</script></body></html>`;

await mkdir(out, { recursive: true });
const manifest = { format: 'day-01-technical-broll/v1', sourceScript: '../../../day-01-spoken-script.md', width: 1920, height: 1080, fps: 30, audio: false, package: 'hyperframes@0.8.141', clips: [] };
if (process.argv.length > 2) {
  try { manifest.clips = JSON.parse(await readFile(path.join(root, 'manifest.json'), 'utf8')).clips; } catch { /* fresh project */ }
}
for (const scene of scenes.filter(s => process.argv.length < 3 || process.argv.slice(2).includes(s.id))) {
  const html = `${scene.id}.html`;
  const mp4 = `renders/${scene.id}.mp4`;
  await writeFile(path.join(root, html), buildHTML(scene), 'utf8');
  const render = spawnSync(bin, ['render', '-c', `./${html}`, '-o', mp4, '--fps', '30', '--workers', '1', '--quality', 'high'], { cwd: root, env, stdio: 'inherit', shell: true, timeout: 480000 });
  if (render.status !== 0) throw new Error(`Render failed: ${scene.id} (${render.error || render.status})`);
  const probe = spawnSync(ffprobe.path, ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate,nb_frames,duration', '-of', 'json', path.join(root, mp4)], { encoding: 'utf8' });
  if (probe.status !== 0) throw new Error(`Probe failed: ${scene.id}: ${probe.stderr}`);
  const stream = JSON.parse(probe.stdout).streams[0];
  if (stream.width !== 1920 || stream.height !== 1080 || stream.r_frame_rate !== '30/1') throw new Error(`Incorrect export: ${scene.id}: ${JSON.stringify(stream)}`);
  manifest.clips = manifest.clips.filter(c => c.id !== scene.id);
  manifest.clips.push({ id: scene.id, source: html, output: mp4, durationSeconds: Number(stream.duration) || scene.duration, fps: 30, frames: Number(stream.nb_frames) || Math.round(scene.duration * 30), editPlacement: scene.placement });
  manifest.clips.sort((a,b) => a.id.localeCompare(b.id));
  await writeFile(path.join(root, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
}
console.log(`Verified ${manifest.clips.length} 1080p30 clips.`);
