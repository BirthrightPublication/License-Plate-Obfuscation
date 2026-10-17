"""Package the runnable browser distribution without overwriting earlier releases."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent.parent
VERSION = '0.1.1'
NAME = 'License-Plate-Obfuscation-Studio-0.1.1-Windows-Portable-r2'


def prepare():
    files = sorted(p.name for p in ROOT.iterdir()
                   if p.is_file() and (p.suffix in ('.md', '.bat', '.txt')
                                       or p.name in ('package.json', 'true-engine.compatibility.json',
                                                     'RELEASE_MANIFEST.json', 'index.html')))
    files += sorted(p.relative_to(ROOT).as_posix() for folder in ('src', 'tools', 'tests', 'docs')
                    for p in (ROOT / folder).rglob('*')
                    if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    baseline = json.loads((ROOT / 'docs/v0.1.0.release.json').read_text(encoding='utf-8'))['files']
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in files}
    manifest = {
        'schemaVersion': 1, 'application': 'birthright.license-plate-studio',
        'version': VERSION, 'packagingRevision': 2, 'previousVersion': '0.1.0', 'kind': 'full', 'patch': None,
        'distribution': 'portable browser application with Python launcher; not a Windows EXE',
        'compatibility': {'osTarget': 'Windows 11', 'python': '>=3.12',
                          'browser': 'current Edge, Chrome, or Firefox', 'trueEngine': None},
        'files': hashes,
        'changedFiles': sorted(p for p in files if hashes[p] != baseline.get(p)),
        'unchangedFiles': sorted(p for p in files if hashes[p] == baseline.get(p)),
        'deletedFiles': [],
        'tests': 'TEST_REPORT.md distinguishes executed Linux tests from unrun Windows checks.',
        'limitations': ['Windows launchers not executed on Windows', 'No True Engine SDK',
                        'No native Windows executable built in Linux', 'V0.1 roadmap not complete']}
    (ROOT / 'release.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return files, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true', help='Refresh only the local integrity manifest')
    args = parser.parse_args()
    files, manifest = prepare()
    if args.prepare:
        return
    subprocess.run(['node', '--test', 'tests/domain.test.js'], cwd=ROOT, check=True)
    import sys
    subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py'],
                   cwd=ROOT, check=True)
    build = ROOT / 'Build'
    build.mkdir(exist_ok=True)
    archive = build / (NAME + '.zip')
    sidecar = build / (NAME + '.release.json')
    checksums = build / (NAME + '.SHA256SUMS.txt')
    if any(p.exists() for p in (archive, sidecar, checksums)):
        raise SystemExit('Release output already exists. Earlier releases are never overwritten.')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
        for name in files + ['release.json']:
            z.write(ROOT / name, name)
    sidecar.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksums.write_text(digest + '  ' + archive.name + '\n', encoding='utf-8')
    print('Created:', archive)
    print('SHA-256:', digest)


if __name__ == '__main__':
    main()
