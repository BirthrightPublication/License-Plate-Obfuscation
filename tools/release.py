"""Prepare local UI integrity metadata or run the standardized Windows build."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def prepare():
    version=json.loads((ROOT/'package.json').read_text())['version']
    assets=['index.html','src/app.js','src/domain.js','src/style.css']
    manifest={'schemaVersion':1,'application':'birthright.license-plate-studio','version':version,
              'files':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in assets},
              'scope':'Development UI asset integrity only; the Windows installer uses app/manifest.json'}
    (ROOT/'release.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    return assets,manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare',action='store_true')
    args=parser.parse_args()
    if args.prepare:prepare()
    else:
        from windows_release import build
        build(ROOT/'Build')
