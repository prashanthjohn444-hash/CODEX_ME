/* Visual themes. Pick per topic with `theme:"neon"|"paper"|"terminal"` in the scene file. Role colours stay: g = input/true, v = memory/process, c = output/false. */
const rgb=h=>[1,3,5].map(i=>parseInt(h.substr(i,2),16)).join(',');
const T={
 neon:{about:'dark, glowing; abstract flows and how-it-works moments',dark:true,bg:'#050609',hd:'#FFFFFF',ink:'#E8ECF5',res:'#CFEEFF',mut:'#8892A6',mut2:'#6C7A90',idx:'#9A86B8',
  g:'#67F04B',v:'#BB58FF',c:'#39BCFF',grid:'rgba(255,255,255,.025)',pf:'rgba(255,255,255,.015)',pfl:'rgba(255,255,255,.07)',ga:.8,sp:1},
 paper:{about:'light, flat, calm; definitions, comparisons, recaps, beginner intros',dark:false,bg:'#FAF6EE',hd:'#1B1F2A',ink:'#1B1F2A',res:'#0F3F63',mut:'#6B7280',mut2:'#8A8F98',idx:'#7A5FB0',
  g:'#2E9E3A',v:'#7B3FD1',c:'#1D7FD6',grid:'rgba(0,0,0,.045)',pf:'rgba(255,255,255,.75)',pfl:'rgba(255,255,255,1)',ga:.3,sp:.35},
 terminal:{about:'black + green mono; command line, installs, tooling cutaways',dark:true,bg:'#020805',hd:'#D6FFE0',ink:'#B6F5C8',res:'#8CFFB0',mut:'#4F8A63',mut2:'#3C7050',idx:'#4F8A63',
  g:'#3DDC84',v:'#FFC857',c:'#7CE7D1',grid:'rgba(61,220,132,.05)',pf:'rgba(61,220,132,.03)',pfl:'rgba(61,220,132,.1)',ga:.6,sp:.7,
  head:"ui-monospace,Menlo,Consolas,'Noto Sans Telugu',monospace"}
};
for(const p of Object.values(T)){p.gr=rgb(p.g);p.vr=rgb(p.v);p.cr=rgb(p.c)}
const cssVars=p=>`:root{--g:${p.g};--v:${p.v};--c:${p.c};--a:#FFBE55;--bg:${p.bg};--hd:${p.hd};--ink:${p.ink};--res:${p.res};--mut:${p.mut};--mut2:${p.mut2};--idx:${p.idx};--gr:${p.gr};--vr:${p.vr};--cr:${p.cr};--grid:${p.grid};--pf:${p.pf};--pfl:${p.pfl};--ga:${p.ga};--sp:${p.sp*100}%;--mono:ui-monospace,Menlo,Consolas,monospace;--head:${p.head||"'Bebas Neue','Noto Sans Telugu','Oswald','Arial Narrow',Impact,sans-serif"};--body:'Barlow','Noto Sans Telugu','Segoe UI',system-ui,sans-serif}`;
module.exports={themes:T,cssVars};
