from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

root = Path(__file__).resolve().parent.parent
subprocess.run(['npm', 'test'], cwd=root, check=True)
files = ['index.html', 'package.json', 'AGENTS.md', 'README.md', 'CHANGELOG.md', 'RELEASE-REPORT.md', 'true-engine.compatibility.json']
files += [str(p.relative_to(root)) for folder in ['src', 'tools', 'tests'] for p in sorted((root / folder).rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
manifest = {'version': '0.1.0', 'kind':'full', 'patch':None, 'files':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files}, 'compatibility':'Browser ES modules; Python 3.12; Node 24 tests. True Engine unintegrated.', 'tests':'npm test: see RELEASE-REPORT.md for actual results', 'changedFiles':files, 'limitations':'Initial release; no prior version exists for a patch. Windows execution untested.'}
build = root / 'Build'
build.mkdir(exist_ok=True)
archive = build / 'License-Plate-Obfuscation-Studio-0.1.0.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(root / p, p)
    z.writestr('release.json', json.dumps(manifest, indent=2))
(build / 'SHA256SUMS.txt').write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n')
(build / 'release.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(archive)
