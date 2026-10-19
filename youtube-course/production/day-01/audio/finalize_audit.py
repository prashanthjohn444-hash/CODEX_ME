import pathlib,json,datetime
R=pathlib.Path(__file__).resolve().parent
p=R/'manifest.json';m=json.loads(p.read_text(encoding='utf-8'))
m['legacy_started_utc']=m.pop('started_utc',m.get('legacy_started_utc'))
m['legacy_finished_utc']=m.pop('finished_utc',m.get('legacy_finished_utc'))
m['reviewed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
m['legacy_signal_verification']=m.pop('verification',m.get('legacy_signal_verification'))
m['legacy_signal_verification']['note']='Historical amplitude/timing only; truncated=false is not a speech completeness finding.'
for s in m['sections']:
 s['legacy_signal_verification']=s.pop('verification',s.get('legacy_signal_verification'))
 s['legacy_signal_verification']['truncation_assessment']='unverified_by_listening_or_transcript'
 s['legacy_signal_verification'].pop('truncated',None)
 s['status']='rendered_pending_speech_qa'
m['provided_reference_asset']='../voice/v2/assets/adam-reference.mp3'
m['test_render']='../voice/v2/test-adam.wav'
m['plan_provenance']='legacy-manifest.json retains original backend plan and events'
p.write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
