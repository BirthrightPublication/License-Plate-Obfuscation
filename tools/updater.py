"""Local release installer. Hashes detect corruption, not publisher authenticity."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
import zipfile


def install(archive, root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=root) as tmp:
        stage = Path(tmp)
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            if len(names) != len(set(names)) or sum(i.file_size for i in z.infolist()) > 50_000_000:
                raise ValueError('Invalid or oversized release')
            for name in names:
                p = PurePosixPath(name)
                if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name:
                    raise ValueError('Unsafe archive path')
            manifest = json.loads(z.read('release.json'))
            version = manifest['version']
            if not isinstance(version, str) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
                raise ValueError('Invalid version')
            if manifest.get('kind', 'full') != 'full':
                raise ValueError('Only full releases are supported; patches are refused')
            expected = manifest['files']
            if set(names) != set(expected) | {'release.json'}:
                raise ValueError('Manifest does not cover archive')
            for name, digest in expected.items():
                data = z.read(name)
                if hashlib.sha256(data).hexdigest() != digest:
                    raise ValueError('Checksum mismatch: ' + name)
                dest = stage / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
            (stage / 'release.json').write_bytes(z.read('release.json'))
        slot = root / 'versions' / version
        slot.parent.mkdir(exist_ok=True)
        if slot.exists():
            raise ValueError('Version already installed; existing files preserved')
        shutil.copytree(stage, slot)
        current = root / 'current.json'
        old = json.loads(current.read_text())['current'] if current.exists() else None
        pointer = root / 'next.json'
        pointer.write_text(json.dumps({'current': version, 'previous': old}))
        os.replace(pointer, current)
    return version


def rollback(root):
    root = Path(root)
    pointer = root / 'current.json'
    state = json.loads(pointer.read_text())
    if not state.get('previous'):
        raise ValueError('No previous release')
    version = state['previous']
    if not isinstance(version, str) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Invalid rollback target')
    target = root / 'versions' / version
    if not target.is_dir():
        raise ValueError('Previous release is missing; current release preserved')
    state['current'], state['previous'] = state['previous'], state['current']
    pending = root / 'next.json'
    pending.write_text(json.dumps(state))
    os.replace(pending, pointer)


def find_release(build):
    candidates = []
    for archive in Path(build).glob('*.zip'):
        try:
            with zipfile.ZipFile(archive) as z:
                manifest = json.loads(z.read('release.json'))
            version = manifest.get('version', '')
            if (manifest.get('application') == 'birthright.license-plate-studio'
                    and manifest.get('kind') == 'full'
                    and re.fullmatch(r'\d+\.\d+\.\d+', version)):
                candidates.append((tuple(map(int, version.split('.'))), archive))
        except (OSError, ValueError, KeyError, zipfile.BadZipFile):
            continue
    if not candidates:
        raise ValueError('No compatible full release ZIP found in Build')
    return max(candidates, key=lambda item: (item[0], item[1].name))[1]


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('archive', nargs='?')
    parser.add_argument('--root', default=str(Path(__file__).resolve().parent.parent / 'Installed'))
    parser.add_argument('--rollback', action='store_true')
    parser.add_argument('--launch', action='store_true')
    parser.add_argument('--build-dir', type=Path)
    args = parser.parse_args()
    if args.build_dir:
        args.archive = str(find_release(args.build_dir))
    if args.rollback:
        rollback(args.root)
    elif args.archive:
        print('Installed', install(args.archive, args.root))
    if args.launch:
        import subprocess
        import sys
        state = json.loads((Path(args.root) / 'current.json').read_text())
        folder = Path(args.root) / 'versions' / state['current']
        subprocess.run([sys.executable, str(Path(__file__).with_name('launch.py')),
                        '--app-root', str(folder)], check=True)

if __name__ == '__main__':
    main()
