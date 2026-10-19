#!/usr/bin/env node
/* node batch.js <scenesDir> <outDir> [--target html|hyperframes|remotion|all]
   Builds every *.js scene in the folder into <outDir>/<name>/ and prints a summary (length, theme, layout, warnings). */
const fs=require('fs'),path=require('path'),cp=require('child_process');
const a=process.argv.slice(2),ti=a.indexOf('--target'),target=ti>=0?a[ti+1]:'html',[dir,out]=a.filter((x,i)=>!x.startsWith('--')&&a[i-1]!=='--target');
if(!dir||!out){console.error('usage: node batch.js scenesDir outDir [--target ...]');process.exit(1)}
const rows=[];
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.js')).sort()){
 const n=f.slice(0,-3),r=cp.spawnSync('node',[path.join(__dirname,'build.js'),path.join(dir,f),path.join(out,n),'--target',target],{encoding:'utf8'});
 const w=(r.stderr||'').split('\n').filter(l=>l.startsWith('!')).map(l=>l.replace(/^! [^:]+: /,''));
 let m={};try{m=require('vm').runInNewContext(fs.readFileSync(path.join(dir,f),'utf8')+';SCENE')}catch{}
 rows.push({n,ok:r.status===0,layout:m.layout,theme:m.theme||'neon',dur:m.duration||4.5,w});
}
console.log('\nscene'.padEnd(26)+'layout'.padEnd(10)+'theme'.padEnd(10)+'secs  status');
for(const r of rows)console.log(r.n.padEnd(25)+String(r.layout).padEnd(10)+r.theme.padEnd(10)+String(r.dur).padEnd(6)+(r.ok?(r.w.length?r.w.length+' warning(s)':'ok'):'FAILED'));
rows.forEach(r=>r.w.forEach(x=>console.log(' - '+r.n+': '+x)));
