"""Post-publication Windows acceptance: public GitHub -> checksum -> native install."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.error

from github_updater import update, verify_app


def main():
    if sys.platform!='win32':raise RuntimeError('Live native acceptance requires Windows')
    expected=json.loads((Path(__file__).resolve().parents[1]/'package.json').read_text())['version']
    sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    with tempfile.TemporaryDirectory(prefix='Live Plate Studio ') as tmp:
        root=Path(tmp)
        files=['Projects/keep.json','Original Media/original.jpg','Processed Media/processed.jpg',
               'Output/result.dat','Presets/mine.json','settings.json','history.json','export-preferences.json']
        for name in files:
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'personal-data')
        deadline=time.monotonic()+60
        while True:
            try:
                assert update(root)
                break
            except urllib.error.HTTPError as error:
                if error.code!=404 or time.monotonic()>=deadline:raise
                time.sleep(2) # a just-published latest release can take a moment to become visible
        manifest=verify_app(root/'app')
        assert manifest['version']==expected and manifest['sourceCommit']==sha
        assert update(root) is False
        for name in files:assert(root/name).read_bytes()==b'personal-data'
        report={'version':expected,'sourceCommit':sha,'platform':'Windows x64',
                'checks':['public latest stable API','real HTTPS asset download','outer checksum',
                          'complete ZIP and per-file manifest','native runtime before/after activation',
                          'original media/projects/settings/preferences/history preserved',
                          'second check reports already current'],
                'sha256':next((root/'Build').glob('*.sha256')).read_text().strip()}
        print(json.dumps(report,indent=2))


if __name__=='__main__':
    try:main()
    except Exception:
        import traceback
        print('::error::'+traceback.format_exc().replace('%','%25').replace('\r','%0D').replace('\n','%0A'),flush=True)
        raise
