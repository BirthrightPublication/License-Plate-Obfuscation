"""Integration check for a real portable ZIP, including its extracted launcher."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--previous', type=Path)
    parser.add_argument('--browser', action='store_true')
    parser.add_argument('--port', type=int, default=4185)
    args = parser.parse_args()
    archive = args.archive.resolve()
    report = {'archive': archive.name, 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
              'platform': sys.platform, 'checks': []}
    with tempfile.TemporaryDirectory(prefix='studio-package-') as tmp:
        base = Path(tmp) / 'License Plate Obfuscation Studio'
        extracted = base / 'Releases/0.1.1'
        with zipfile.ZipFile(archive) as z:
            z.extractall(extracted)
        verifier = load('packaged_verifier', extracted / 'tools/verify_release.py')
        report['filesVerified'] = verifier.verify(extracted)
        report['checks'].append('all packaged file hashes match')
        subprocess.run([sys.executable, str(extracted / 'tools/launch.py'), '--check'], check=True)
        updater = load('packaged_updater', extracted / 'tools/updater.py')
        installed = extracted / 'Installed'
        projects = base / 'Projects'
        projects.mkdir(parents=True)
        marker = projects / 'keep.json'
        marker.write_text('{"personal":"preserve"}')
        settings = base / 'settings.json'
        settings.write_text('{"setting":"preserve"}')
        if args.previous:
            updater.install(args.previous.resolve(), installed)
        updater.install(archive, installed)
        before = (installed / 'current.json').read_bytes()
        try:
            updater.install(archive, installed)
        except ValueError:
            pass
        else:
            raise AssertionError('Existing version was overwritten')
        assert (installed / 'current.json').read_bytes() == before
        if args.previous:
            updater.rollback(installed)
            assert json.loads((installed / 'current.json').read_text())['current'] == '0.1.0'
            subprocess.run([sys.executable, str(extracted / 'tools/launch.py'), '--check'], check=True)
            updater.rollback(installed)
            assert json.loads((installed / 'current.json').read_text())['current'] == '0.1.1'
            report['checks'].append('actual 0.1.0 to 0.1.1 installation and rollback both directions')
        assert marker.read_text() == '{"personal":"preserve"}'
        assert settings.read_text() == '{"setting":"preserve"}'
        report['checks'].append('project/settings marker files and earlier version preserved')
        report['checks'].append('repeat install refused without changing active pointer')
        env = dict(os.environ)
        env['STUDIO_URL'] = 'http://localhost:' + str(args.port)
        command = [sys.executable, str(extracted / 'tools/launch.py'), '--no-browser', '--port', str(args.port)]
        process = subprocess.Popen(command, cwd=base, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        try:
            deadline = time.monotonic() + 10
            while True:
                if process.poll() is not None:
                    raise RuntimeError(process.stdout.read())
                try:
                    with urllib.request.urlopen(env['STUDIO_URL'], timeout=1) as response:
                        assert b'v0.1.1' in response.read()
                    break
                except OSError:
                    if time.monotonic() > deadline:
                        raise
                    time.sleep(0.1)
            report['checks'].append('extracted launcher starts from a path with spaces and serves active UI')
            if args.browser:
                subprocess.run(['node', str(extracted / 'tools/smoke.cjs')], env=env, check=True)
                report['checks'].append('extracted release full Chromium browser smoke test')
        finally:
            process.terminate()
            process.communicate(timeout=5)
        verifier.verify(extracted)
        report['checks'].append('all packaged hashes unchanged after running')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
