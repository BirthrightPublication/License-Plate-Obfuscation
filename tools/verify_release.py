"""Verify all listed release files; never alter application or user data."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def verify(root):
    manifest = json.loads((root / 'release.json').read_text(encoding='utf-8'))
    for name, expected in manifest['files'].items():
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
            raise ValueError('Invalid manifest path')
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Checksum mismatch: ' + name)
    return len(manifest['files'])


if __name__ == '__main__':
    try:
        count = verify(Path(__file__).resolve().parent.parent)
        print('PASS: all', count, 'packaged file hashes match release.json.')
    except (OSError, ValueError, KeyError) as error:
        print('Verification failed:', error, file=sys.stderr)
        raise SystemExit(1)
