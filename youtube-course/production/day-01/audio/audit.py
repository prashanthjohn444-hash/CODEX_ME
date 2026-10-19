import pathlib,json,hashlib,wave,array,math,shutil,re,subprocess,io,contextlib
R=pathlib.Path(__file__).resolve().parent
BASE=R.parent/'voice/v2'
SRC=R.parents[2]/'day-01-spoken-script.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
assert sha(SRC)==m['source_sha256']
shutil.copyfile(SRC,R/'spoken-script.md')
lesson=json.loads((R.parents[2]/'source/lessons.json').read_text(encoding='utf-8'))[0]
(R/'structured-lesson-day-01.json').write_text(json.dumps(lesson,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ['manifest.json','generation.log']:
 shutil.copyfile(BASE/name,R/('legacy-'+name))
files=[s['file'] for s in m['sections']]+['day-01-narration.wav','day-01-narration.m4b']
for name in files: shutil.copyfile(BASE/name,R/name)
checks=[]
for s in m['sections']:
 p=R/s['file']
 with wave.open(str(p)) as w:
  a=array.array('h',w.readframes(w.getnframes())); rate=w.getframerate()
  check={'file':p.name,'sha256':sha(p),'frames':len(a),'sample_rate_hz':rate,'channels':w.getnchannels(),'sample_width_bytes':w.getsampwidth(),'duration_seconds':len(a)/rate,'peak_abs':max(map(abs,a)),'clipped_samples':sum(abs(x)>=32767 for x in a),'rms':math.sqrt(sum(x*x for x in a)/len(a))}
 checks.append(check)
 s['sha256']=check['sha256']
 s['qa']={'signal':check,'transcript_status':'pending','listening_status':'pending'}
codechecks=[]
for i,code in enumerate(re.findall(r'```python\n(.*?)```',SRC.read_text(encoding='utf-8'),re.S)):
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,'<lesson-example>','exec'),{})
 codechecks.append({'block':i+1,'code':code,'stdout':out.getvalue(),'status':'passed'})
m.update({'status':'qa_in_progress','script':'spoken-script.md','script_sha256':sha(R/'spoken-script.md'),'legacy_provenance':str(BASE),'reuse_status':'matching_script_and_generation_settings_signal_audited_pending_speech_qa','qa':{'signal_checks':checks,'python_examples':codechecks,'listening_status':'pending','transcript_status':'pending'},'source_hashes':{str(p):sha(p) for p in [SRC,R.parents[2]/'episodes/day-01.md',R.parents[2]/'source/day-01.txt',R/'structured-lesson-day-01.json']}})
(R/'manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'duration':m['concatenated_audio']['duration_seconds'],'sections':len(checks),'clipped_samples':sum(c['clipped_samples'] for c in checks),'python_examples':codechecks},indent=2))
