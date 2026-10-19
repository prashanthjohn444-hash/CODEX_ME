import requests,pathlib,json,re,difflib,time
R=pathlib.Path(__file__).resolve().parent
u='http://127.0.0.1:3900'
profiles=requests.get(u+'/profiles',timeout=30);profiles.raise_for_status()
catalog=profiles.json();(R/'current-voice-catalog.json').write_text(json.dumps(catalog,indent=2),encoding='utf-8')
assert any(p['id']=='d8f312f3' and 'ADAM-ENGLISH' in p['name'] for p in catalog), 'Adam catalog mismatch'
m=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
for s in m['sections']:
 p=R/f"transcript-{s['id']}.json"
 if not p.exists():
  with open(R/s['file'],'rb') as f:r=requests.post(u+'/transcribe',files={'audio':(s['file'],f,'audio/wav')},data={'mode':'reference','language':'en'},timeout=1800)
  if not r.ok:
   (R/'transcription-error.json').write_text(r.text,encoding='utf-8');r.raise_for_status()
  p.write_text(json.dumps(r.json(),indent=2),encoding='utf-8')
 d=json.loads(p.read_text(encoding='utf-8'))
 norm=lambda t:re.findall(r"[a-z0-9]+",t.lower())
 a,b=norm(s['text']),norm(d['text']);matcher=difflib.SequenceMatcher(None,a,b,autojunk=False)
 s['qa'].update({'transcript_status':'review_required','transcript_file':p.name,'transcript_similarity':matcher.ratio(),'differences':[{'operation':op,'expected':' '.join(a[i:j]),'heard':' '.join(b[k:l])} for op,i,j,k,l in matcher.get_opcodes() if op!='equal']})
 (R/'manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
 print(s['id'],d['text'],flush=True)
