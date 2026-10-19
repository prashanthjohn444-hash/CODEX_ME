#!/usr/bin/env node
/* Brand-logo resolver. Usage:
     node logos.js python            -> JSON {slug,title,hex,path}
     node logos.js --bundle a,b,c    -> add slugs to assets/logos/bundle.json (needs npm access once)
   Resolution order: assets/logos/custom/<slug>.svg (user-supplied) -> assets/logos/bundle.json -> simple-icons from npm.
   Never draws or approximates a logo: if nothing matches, resolve() returns null and the caller shows no logo. */
const fs=require('fs'),path=require('path'),cp=require('child_process');
const ROOT=path.join(__dirname,'..','assets','logos'),BUNDLE=path.join(ROOT,'bundle.json');
const ALIAS={py:'python',python3:'python',js:'javascript',ts:'typescript',node:'nodedotjs',nodejs:'nodedotjs','node.js':'nodedotjs',
 gh:'github',vscode:'visualstudiocode','vs code':'visualstudiocode',pip:'pypi',postgres:'postgresql',k8s:'kubernetes',mongo:'mongodb',
 'c++':'cplusplus',cpp:'cplusplus',html:'html5',twitter:'x','x (twitter)':'x',yt:'youtube',ig:'instagram',fb:'facebook',
 bash:'gnubash',shell:'gnubash',terminal:'gnubash',vue:'vuedotjs',hf:'huggingface',gcp:'googlecloud',claude:'claude',chatgpt:'openai'};
const norm=s=>String(s).trim().toLowerCase().replace(/^@/,'');
const bundle=()=>{try{return JSON.parse(fs.readFileSync(BUNDLE,'utf8'))}catch{return{}}};
function fromSimpleIcons(slug){
 let si;try{si=require('simple-icons')}catch{
  const tmp=path.join(require('os').tmpdir(),'si-cache');fs.mkdirSync(tmp,{recursive:true});
  try{cp.execSync('npm i simple-icons --no-audit --no-fund --silent',{cwd:tmp,stdio:'ignore'});si=require(path.join(tmp,'node_modules','simple-icons'))}catch{return null}}
 const key='si'+slug.replace(/(^|[^a-z0-9])([a-z0-9])/g,(m,a,b)=>b.toUpperCase());
 const i=si[key]||Object.values(si).find(x=>x&&x.slug===slug);
 return i?{slug:i.slug,title:i.title,hex:i.hex,path:i.path}:null}
function resolve(keyword){
 const k=norm(keyword),slug=ALIAS[k]||k.replace(/[^a-z0-9]/g,'');
 const custom=path.join(ROOT,'custom',slug+'.svg');
 if(fs.existsSync(custom)){const svg=fs.readFileSync(custom,'utf8'),d=[...svg.matchAll(/ d="([^"]+)"/g)].map(m=>m[1]).join(' '),vb=(svg.match(/viewBox="([^"]+)"/)||[])[1]||'0 0 24 24';
  if(d)return{slug,title:slug,hex:'FFFFFF',path:d,viewBox:vb,custom:true}}
 const b=bundle();if(b[slug])return{...b[slug],viewBox:'0 0 24 24'};
 const i=fromSimpleIcons(slug);if(i){b[slug]={slug:i.slug,title:i.title,hex:i.hex,path:i.path};try{fs.writeFileSync(BUNDLE,JSON.stringify(b))}catch{}return{...i,viewBox:'0 0 24 24'}}
 return null}
const lum=h=>{const c=[0,2,4].map(i=>parseInt(h.substr(i,2),16)/255).map(v=>v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4));return .2126*c[0]+.7152*c[1]+.0722*c[2]};
/* brand colour as published; on dark themes near-black brands (GitHub, X, TikTok…) render white, on light themes near-white brands render dark ink */
const displayColor=(hex,dark=true)=>dark?(lum(hex)<.1?'#FFFFFF':'#'+hex):(lum(hex)>.75?'#1B1F2A':'#'+hex);
const svgFor=(l,cls='logo',dark=true)=>`<svg class="${cls}" viewBox="${l.viewBox||'0 0 24 24'}" role="img" aria-label="${l.title} logo"><path d="${l.path}" fill="${displayColor(l.hex,dark)}"/></svg>`;
module.exports={resolve,svgFor,displayColor};
if(require.main===module){
 const a=process.argv.slice(2);
 if(a[0]==='--bundle'){let n=0;for(const k of a[1].split(',')){const r=resolve(k);console.log(k,r?'OK '+r.title:'NOT FOUND');n+=!!r}console.log(n+' logos in bundle')}
 else{const r=resolve(a.join(' '));console.log(r?JSON.stringify({...r,path:r.path.slice(0,40)+'…'}):'NOT FOUND: supply an SVG at assets/logos/custom/<slug>.svg')}}
