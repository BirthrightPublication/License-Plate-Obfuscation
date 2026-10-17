"""Build the complete, versioned Windows-x64 installation package on Windows."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def run(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def build(output):
    if sys.platform != 'win32' or platform.machine().upper() not in ('AMD64', 'X86_64'):
        raise ValueError('Windows x64 with x64 Python is required; cross-compilation is not supported')
    from github_updater import ROOT_FILES, verify_app, extract_package, version_tuple
    version = json.loads((ROOT / 'package.json').read_text())['version']
    version_tuple(version)
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True).strip():
        raise ValueError('Build requires a clean tracked source commit')
    name = 'License-Plate-Studio-v' + version + '-windows-x64.zip'
    output.mkdir(parents=True, exist_ok=True)
    archive = output / name
    if archive.exists() or (output / (name + '.sha256')).exists():
        raise ValueError('Refusing to replace an existing release')
    with tempfile.TemporaryDirectory(prefix='plate-build-') as tmp:
        work = Path(tmp)
        runtime = work / 'runtime'
        runtime.mkdir()
        assets = ['index.html', 'src/app.js', 'src/domain.js', 'src/style.css']
        runtime_manifest = {'version': version, 'application': 'birthright.license-plate-studio',
                            'files': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in assets}}
        (runtime / 'release.json').write_text(json.dumps(runtime_manifest), encoding='utf-8')
        stage = work / 'package'
        app = stage / 'app'
        app.mkdir(parents=True)
        for name_exe, source in [('PlateStudio', 'tools/launch.py'), ('PlateUpdater', 'tools/github_updater.py')]:
            args = [sys.executable, '-m', 'PyInstaller', '--onefile', '--console', '--noupx',
                    '--name', name_exe, '--distpath', str(app), '--workpath', str(work / name_exe),
                    '--specpath', str(work)]
            if name_exe == 'PlateStudio':
                data = [(ROOT / p, 'src' if p.startswith('src/') else '.') for p in assets]
                for p, dest in data + [(runtime / 'release.json', '.')]:
                    args += ['--add-data', str(p) + ':' + dest]
            run(args + [str(ROOT / source)], cwd=ROOT)
        for p in ['true-engine.compatibility.json', 'CHANGELOG.md', 'KNOWN_ISSUES.md']:
            shutil.copy2(ROOT / p, app / p)
        manifest = {'schemaVersion': 1, 'application': 'birthright.license-plate-studio',
                    'version': version, 'platform': 'windows-x64', 'sourceCommit': sha,
                    'updaterProtocol': 1, 'trueEngine': None,
                    'distribution': 'PyInstaller self-contained runtime, default-system-browser UI',
                    'files': {p.relative_to(app).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in sorted(app.rglob('*')) if p.is_file()}}
        (app / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        for p in ROOT_FILES:
            shutil.copy2(ROOT / p, stage / p)
        verify_app(app)
        for exe in ['PlateStudio.exe', 'PlateUpdater.exe']:
            run([str(app / exe), '--check'])
        with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(stage.rglob('*')):
                if p.is_file():
                    z.write(p, p.relative_to(stage).as_posix())
        extract_package(archive, work / 'verified', version)
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / (name + '.sha256')).write_text(checksum + '  ' + name + '\n', encoding='ascii')
    print('Built:', archive)
    print('SHA-256:', checksum)
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'Build')
    args = parser.parse_args()
    build(args.output.resolve())
