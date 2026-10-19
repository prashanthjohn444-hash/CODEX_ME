"""Push the initial project in bounded Git packs; keep the original history locally."""
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / '.git' / 'john-upload-state.json'
INDEX = ROOT / '.git' / 'john-upload-index'


def git(*args, data=None, env=None):
    return subprocess.check_output(['git', *args], cwd=ROOT, input=data,
                                   env=env).decode().strip()


def main():
    if STATE.exists():
        state = json.loads(STATE.read_text())
    else:
        source = git('rev-parse', 'main')
        git('branch', 'john-initial-backup', source)
        entries = []
        for record in subprocess.check_output(
                ['git', 'ls-tree', '-r', '-l', '-z', source], cwd=ROOT).split(b'\0'):
            if not record:
                continue
            meta, path = record.split(b'\t', 1)
            mode, kind, oid, size = meta.split()
            entries.append({'mode': mode.decode(), 'oid': oid.decode(),
                            'size': int(size), 'path': path.decode('utf-8')})
        small = [e for e in entries if e['size'] < 256 * 1024]
        big = sorted([e for e in entries if e['size'] >= 256 * 1024],
                     key=lambda e: e['size'])
        batches = [small]
        batch, size = [], 0
        for entry in big:
            if batch and size + entry['size'] > 32 * 1024 * 1024:
                batches.append(batch)
                batch, size = [], 0
            batch.append(entry)
            size += entry['size']
        if batch:
            batches.append(batch)
        env = os.environ.copy()
        env['GIT_INDEX_FILE'] = str(INDEX)
        git('read-tree', '--empty', env=env)
        parent = None
        commits = []
        for i, batch in enumerate(batches, 1):
            data = b''.join((e['mode']+' '+e['oid']+'\t'+e['path']).encode('utf-8')+b'\0'
                            for e in batch)
            git('update-index', '-z', '--index-info', data=data, env=env)
            tree = git('write-tree', env=env)
            args = ['commit-tree', tree]
            if parent:
                args += ['-p', parent]
            parent = git(*args, '-m', f'Add project files (batch {i}/{len(batches)})')
            commits.append({'sha': parent, 'bytes': sum(e['size'] for e in batch),
                            'files': len(batch)})
        assert git('rev-parse', f'{parent}^{{tree}}') == git('rev-parse', f'{source}^{{tree}}')
        state = {'source': source, 'commits': commits, 'completed': 0}
        STATE.write_text(json.dumps(state, indent=2))
    for i in range(state['completed'], len(state['commits'])):
        item = state['commits'][i]
        print(f"Pushing batch {i+1}/{len(state['commits'])}: {item['files']} files, "
              f"{item['bytes']/1024**2:.1f} MiB", flush=True)
        result = subprocess.run(['git', '-c', 'http.version=HTTP/1.1',
                                 '-c', 'http.postBuffer=104857600',
                                 'push', 'origin', item['sha']+':refs/heads/main'],
                                cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            actual = git('ls-remote', 'origin', 'refs/heads/main')
            if not actual.startswith(item['sha']):
                print(result.stderr[-3000:], flush=True)
                raise SystemExit(result.returncode)
        state['completed'] = i+1
        STATE.write_text(json.dumps(state, indent=2))
        print(f"Confirmed batch {i+1}/{len(state['commits'])}", flush=True)
    last = state['commits'][-1]['sha']
    git('update-ref', 'refs/heads/main', last, state['source'])
    git('fetch', 'origin', 'main')
    git('branch', '--set-upstream-to=origin/main', 'main')
    assert git('ls-remote', 'origin', 'refs/heads/main').startswith(last)
    assert not git('status', '--porcelain')
    print('SUCCESS: remote main matches local main; working tree clean. '+last, flush=True)


if __name__ == '__main__':
    main()
