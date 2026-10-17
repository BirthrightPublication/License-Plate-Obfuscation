"""Run on Windows to freeze the existing browser host, not to build True Engine."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


def main():
    if sys.platform != 'win32':
        raise SystemExit('Native Windows builds require Windows and Python 3.12+. '
                         'PyInstaller cannot cross-compile Windows executables on Linux.')
    if sys.version_info < (3, 12):
        raise SystemExit('Python 3.12+ required; Python 3.12 x64 recommended.')
    root = Path(__file__).resolve().parent.parent
    subprocess.run([sys.executable, str(root / 'tools/launch.py'), '--check'], check=True)
    build = root / 'Build'
    build.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    output = Path(tempfile.mkdtemp(prefix='Native-0.1.1-' + stamp + '-', dir=build))
    with tempfile.TemporaryDirectory(prefix='native-work-', dir=build) as tmp:
        work = Path(tmp)
        subprocess.run([sys.executable, '-m', 'venv', str(work / 'venv')], check=True)
        python = work / 'venv/Scripts/python.exe'
        subprocess.run([str(python), '-m', 'pip', 'install', 'pyinstaller==6.16.0'], check=True)
        args = [str(python), '-m', 'PyInstaller', '--onefile', '--console',
                '--name', 'LicensePlateObfuscationStudio-0.1.1',
                '--distpath', str(output / 'app'), '--workpath', str(work / 'pyinstaller'),
                '--specpath', str(work)]
        for name in ['index.html', 'src', 'release.json']:
            args += ['--add-data', str(root / name) + ':' + ('src' if name == 'src' else '.')]
        subprocess.run(args + [str(root / 'tools/launch.py')], check=True)
        exe = output / 'app/LicensePlateObfuscationStudio-0.1.1.exe'
        result = subprocess.run([str(exe), '--check'], check=True, capture_output=True, text=True)
    report = {'version': '0.1.1', 'kind': 'native-browser-host', 'engine': 'not integrated',
              'buildPython': sys.version, 'pyinstaller': '6.16.0',
              'testsExecuted': {'embeddedAssetCheck': result.stdout.strip()},
              'testsNotExecuted': ['Windows interactive browser workflow', 'SmartScreen/signing'],
              'signature': 'unsigned', 'sourceRelease': '0.1.1 portable'}
    folder = output / 'app'
    for name in ['README - FIRST TIME SETUP.txt', 'true-engine.compatibility.json',
                 'CHANGELOG.md', 'KNOWN_ISSUES.md']:
        shutil.copy2(root / name, folder / name)
    report['files'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted(folder.iterdir()) if p.is_file()}
    (folder / 'native-manifest.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    archive = output / 'License-Plate-Obfuscation-Studio-0.1.1-Windows-Native.zip'
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(folder.iterdir()):
            z.write(p, p.name)
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / 'SHA256SUMS.txt').write_text(checksum + '  ' + archive.name + '\n')
    print('Built:', archive)
    print('SHA-256:', checksum)
    print('This is an unsigned browser-host EXE, not a True Engine executable.')


if __name__ == '__main__':
    main()
