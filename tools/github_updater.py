"""Transactional public-GitHub Windows updater. No third-party runtime packages."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import logging
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse
import uuid
import zipfile

REPOSITORY = 'BirthrightPublication/License-Plate-Obfuscation'
PRODUCT = 'birthright.license-plate-studio'
VERSION = '0.1.2'
API = 'https://api.github.com/repos/' + REPOSITORY + '/releases/latest'
HOSTS = {'api.github.com', 'github.com', 'release-assets.githubusercontent.com',
         'objects.githubusercontent.com'}
MAX_PACKAGE = 512 * 1024 * 1024
MAX_UNPACKED = 1024 * 1024 * 1024
ROOT_FILES = {'Start Plate.bat', 'Update Plate.bat', 'Rollback Plate.bat',
              'README - FIRST TIME SETUP.txt'}
LOG = logging.getLogger('plate-update')


def version_tuple(value):
    if not isinstance(value, str) or not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', value):
        raise ValueError('Expected a stable MAJOR.MINOR.PATCH version')
    return tuple(map(int, value.split('.')))


def control(root):
    root = Path(root)
    if root.is_symlink():
        raise ValueError('Installation root cannot be a link')
    p = root / '.plate-studio'
    p.mkdir(parents=True, exist_ok=True)
    if p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()):
        raise ValueError('Updater control directory cannot be a link')
    return p


def directory(parent, name):
    p = parent / name
    if p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()):
        raise ValueError('Managed directory cannot be a link: ' + name)
    p.mkdir(parents=True, exist_ok=True)
    return p


def atomic_json(path, value):
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(value, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


@contextmanager
def update_lock(root):
    path = control(root) / 'update.lock'
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    acquired = False
    try:
        if os.fstat(fd).st_size == 0:
            os.write(fd, b'0')
        os.lseek(fd, 0, os.SEEK_SET)
        try:
            if sys.platform == 'win32':
                import msvcrt
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise ValueError('Another updater is running; wait for it to finish')
        acquired = True
        yield
    finally:
        if acquired:
            os.lseek(fd, 0, os.SEEK_SET)
            if sys.platform == 'win32':
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def safe_name(name):
    p = PurePosixPath(name)
    if (not name or p.is_absolute() or '\\' in name or ':' in name
            or any(part in ('', '.', '..') for part in name.split('/'))
            or any(part.endswith((' ', '.')) for part in p.parts)
            or any(re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part, re.I) for part in p.parts)
            or any(ord(c) < 32 or c in '<>"|?*' for c in name)):
        raise ValueError('Unsafe package path: ' + repr(name))
    return p


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def verify_app(folder):
    folder = Path(folder)
    if folder.is_symlink() or (hasattr(folder, 'is_junction') and folder.is_junction()):
        raise ValueError('Managed app cannot be a link')
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    if (manifest.get('schemaVersion') != 1 or manifest.get('application') != PRODUCT
            or manifest.get('platform') != 'windows-x64' or manifest.get('updaterProtocol') != 1):
        raise ValueError('Incompatible application manifest')
    version_tuple(manifest.get('version'))
    if not re.fullmatch(r'[a-f0-9]{40}', manifest.get('sourceCommit', '')):
        raise ValueError('Missing exact source commit')
    files = manifest.get('files')
    if not isinstance(files, dict) or not {'PlateStudio.exe', 'PlateUpdater.exe'} <= files.keys():
        raise ValueError('Package lacks the complete application/runtime launchers')
    expected = set(files) | {'manifest.json'}
    actual = set()
    for p in folder.rglob('*'):
        if p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()):
            raise ValueError('Links are not supported in managed app')
        if p.is_file():
            actual.add(p.relative_to(folder).as_posix())
    if actual != expected:
        raise ValueError('Unmanaged or missing files in app; preserve/move personal files before updating')
    for name, digest in files.items():
        safe_name(name)
        if not re.fullmatch(r'[0-9a-f]{64}', digest) or sha256(folder / name) != digest:
            raise ValueError('Application checksum mismatch: ' + name)
    return manifest


def extract_package(archive, destination, expected_version):
    version_tuple(expected_version)
    with zipfile.ZipFile(archive) as z:
        info = z.infolist()
        if len(info) > 5000 or sum(i.file_size for i in info) > MAX_UNPACKED:
            raise ValueError('Package exceeds unpacked limits')
        names = [i.filename for i in info]
        if len({n.casefold() for n in names}) != len(names):
            raise ValueError('Duplicate/case-colliding ZIP entries')
        for i in info:
            safe_name(i.filename)
            if i.is_dir() or stat.S_ISLNK(i.external_attr >> 16):
                raise ValueError('Only regular files may be packaged')
            if not (i.filename.startswith('app/') or i.filename in ROOT_FILES):
                raise ValueError('Package attempts to write outside managed application')
        if 'app/manifest.json' not in names or not ROOT_FILES <= set(names):
            raise ValueError('Incomplete installation ZIP')
        for i in info:
            dest = destination / i.filename
            dest.parent.mkdir(parents=True, exist_ok=True)
            with z.open(i) as source, dest.open('wb') as target:
                shutil.copyfileobj(source, target, 1024 * 1024)
    manifest = verify_app(destination / 'app')
    if manifest['version'] != expected_version:
        raise ValueError('Release tag and package version differ')
    return manifest


class TrustedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def check_url(url):
    p = urlparse(url)
    if p.scheme != 'https' or p.hostname not in HOSTS or p.username or p.password or p.port not in (None, 443):
        raise ValueError('Untrusted download destination')


def fetch(url, limit, destination=None):
    check_url(url)
    request = urllib.request.Request(url, headers={'User-Agent': 'Birthright-PlateStudio-Updater/' + VERSION,
                                                  'Accept': 'application/vnd.github+json' if url == API else 'application/octet-stream'})
    opener = urllib.request.build_opener(TrustedRedirect())
    with opener.open(request, timeout=30) as response:
        check_url(response.geturl())
        total = 0
        data = bytearray()
        out = destination.open('wb') if destination else None
        try:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > limit:
                    raise ValueError('Download exceeds size limit')
                if out:
                    out.write(chunk)
                else:
                    data.extend(chunk)
        finally:
            if out:
                out.close()
        return bytes(data) if not destination else total


def select_release(release):
    if release.get('draft') or release.get('prerelease'):
        raise ValueError('Only stable published releases can be installed')
    tag = release.get('tag_name', '')
    if not tag.startswith('v'):
        raise ValueError('Release tag must start with v')
    version = tag[1:]
    version_tuple(version)
    name = 'License-Plate-Studio-v' + version + '-windows-x64.zip'
    assets = release.get('assets', [])
    selected = {}
    for filename in (name, name + '.sha256'):
        matches = [a for a in assets if a.get('name') == filename and a.get('state', 'uploaded') == 'uploaded']
        if len(matches) != 1:
            raise ValueError('Stable release is missing a unique required asset: ' + filename)
        url = matches[0]['browser_download_url']
        prefix = 'https://github.com/' + REPOSITORY + '/releases/download/' + tag + '/'
        if not url.startswith(prefix) or url[len(prefix):] != filename:
            raise ValueError('Asset URL is not from the selected repository and tag')
        selected[filename] = url
    return version, name, selected


def parse_checksum(data, filename):
    try:
        text = data.decode('ascii').strip()
    except UnicodeError:
        raise ValueError('Invalid checksum text')
    match = re.fullmatch(r'([a-fA-F0-9]{64})(?:[ \t]+\*?([^\r\n]+))?', text)
    if not match or (match[2] is not None and match[2] != filename):
        raise ValueError('Checksum file is malformed or names another ZIP')
    return match[1].lower()


def native_probe(app):
    if sys.platform != 'win32':
        raise RuntimeError('Native application validation requires Windows x64')
    process = subprocess.Popen([str(app / 'PlateStudio.exe'), '--check'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        stdout, stderr = process.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        # Terminate only our own probe process tree, including the PyInstaller bootloader child.
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
        process.communicate(timeout=15)
        raise ValueError('Application self-check timed out')
    version = verify_app(app)['version']
    if process.returncode or ('PASS: v' + version + ' application assets verified.') not in stdout:
        raise ValueError('Application self-check failed: ' + stdout + stderr)


def move_code(source, target):
    # A bootstrap parent or a closing browser host can briefly hold an EXE open on Windows.
    deadline = time.monotonic() + 10
    while True:
        try:
            os.replace(source, target)
            return
        except PermissionError:
            if time.monotonic() >= deadline:
                raise ValueError('Close all Plate Studio windows/consoles and retry. Files are in use.')
            time.sleep(0.2)


def recover(root):
    ctl = control(root)
    journal = ctl / 'transaction.json'
    if not journal.exists():
        return
    record = json.loads(journal.read_text(encoding='utf-8'))
    txn = record.get('id', '')
    if not re.fullmatch(r'[a-f0-9]{32}', txn):
        raise ValueError('Invalid recovery journal; no application files changed')
    if record.get('status') == 'committed':
        journal.unlink()
        return
    backup = directory(ctl, 'backups') / txn / 'app'
    app = root / 'app'
    if backup.exists():
        verify_app(backup)
        if app.exists():
            failed = directory(ctl, 'failed') / txn
            if failed.exists():
                raise ValueError('Recovery target exists; refusing to overwrite retained files')
            move_code(app, failed)
        move_code(backup, app)
        LOG.warning('Recovered previous app from interrupted/failed update')
    elif record.get('hadApp'):
        # If backup rename never happened, old app is still active. Verify instead of deleting.
        verify_app(app)
        if verify_app(app)['version'] != record['oldVersion']:
            raise ValueError('Recovery requires manual inspection; original backup is missing')
    elif app.exists():
        failed = directory(ctl, 'failed') / txn
        move_code(app, failed)
    journal.unlink()


def install(root, archive, expected_version, probe=native_probe):
    root = Path(root)
    ctl = control(root)
    recover(root)
    app = root / 'app'
    previous = verify_app(app) if app.exists() else None
    if previous and version_tuple(expected_version) <= version_tuple(previous['version']):
        raise ValueError('Refusing reinstall or downgrade; use explicit rollback')
    txn = uuid.uuid4().hex
    with tempfile.TemporaryDirectory(prefix='stage-', dir=ctl) as tmp:
        stage = Path(tmp)
        LOG.info('Validating and staging v%s', expected_version)
        manifest = extract_package(archive, stage, expected_version)
        LOG.info('Checking staged Windows runtime')
        probe(stage / 'app')
        for name in sorted(ROOT_FILES):
            destination = root / name
            if not destination.exists():
                with destination.open('xb') as f:
                    f.write((stage / name).read_bytes())
        backup = directory(ctl, 'backups') / txn / 'app'
        backup.parent.mkdir(parents=True)
        record = {'id': txn, 'status': 'prepared', 'hadApp': previous is not None,
                  'oldVersion': previous['version'] if previous else None, 'newVersion': expected_version}
        journal = ctl / 'transaction.json'
        atomic_json(journal, record)
        try:
            if previous:
                LOG.info('Backing up installed app to %s', backup)
                move_code(app, backup)
            LOG.info('Activating and checking the new application')
            move_code(stage / 'app', app)
            probe(app)
            verify_app(app)
            record['status'] = 'committed'
            atomic_json(journal, record)
        except BaseException:
            recover(root)
            raise
        # Root launchers are never overwritten. Existing code, projects/media/configs outside app are untouched.
        journal.unlink(missing_ok=True)
        LOG.info('Installed and verified v%s; retained backup %s', expected_version, backup.parent)
        return manifest


def rollback(root, probe=native_probe):
    ctl = control(root)
    recover(root)
    current = verify_app(root / 'app')
    backups = sorted(directory(ctl, 'backups').glob('*/app'), key=lambda p: p.stat().st_mtime, reverse=True)
    candidates = [p for p in backups if verify_app(p)['version'] != current['version']]
    if not candidates:
        raise ValueError('No previous verified app backup exists')
    target = candidates[0]
    probe(target)
    txn = uuid.uuid4().hex
    saved = directory(ctl, 'backups') / txn / 'app'
    saved.parent.mkdir(parents=True)
    record = {'id': txn, 'status': 'prepared', 'hadApp': True,
              'oldVersion': current['version'], 'newVersion': verify_app(target)['version']}
    journal = ctl / 'transaction.json'
    atomic_json(journal, record)
    try:
        move_code(root / 'app', saved)
        # Copy the recovery candidate: retain the backup even after successful rollback.
        shutil.copytree(target, root / 'app')
        probe(root / 'app')
        verify_app(root / 'app')
        record['status'] = 'committed'
        atomic_json(journal, record)
    except BaseException:
        recover(root)
        raise
    journal.unlink(missing_ok=True)
    LOG.info('Rollback verified. All backups retained.')


def update(root, transport=fetch, probe=native_probe):
    root = Path(root)
    recover(root)
    existing = verify_app(root / 'app') if (root / 'app').exists() else None
    LOG.info('Checking latest stable GitHub release')
    release = json.loads(transport(API, 2 * 1024 * 1024))
    version, name, assets = select_release(release)
    if existing and version_tuple(version) <= version_tuple(existing['version']):
        LOG.info('Already current: installed v%s, latest v%s', existing['version'], version)
        return False
    build = directory(root, 'Build')
    downloads = directory(control(root), 'downloads')
    with tempfile.TemporaryDirectory(prefix='download-', dir=downloads) as tmp:
        archive = Path(tmp) / name
        LOG.info('Downloading %s', name)
        checksum_data = transport(assets[name + '.sha256'], 4096)
        expected = parse_checksum(checksum_data, name)
        transport(assets[name], MAX_PACKAGE, archive)
        if sha256(archive) != expected:
            raise ValueError('Downloaded ZIP checksum mismatch; installation unchanged')
        LOG.info('SHA-256 verified')
        # Keep each downloaded build permanently; refuse a conflicting existing file.
        for source, dest in [(archive, build / name)]:
            if dest.exists():
                if sha256(dest) != expected:
                    raise ValueError('Build contains a different archive with the same name; preserving it')
            else:
                with dest.open('xb') as f, source.open('rb') as s:
                    shutil.copyfileobj(s, f)
        checksum_path = build / (name + '.sha256')
        if checksum_path.exists():
            if parse_checksum(checksum_path.read_bytes(), name) != expected:
                raise ValueError('Build contains a conflicting checksum; preserving it and the installed app')
        else:
            with checksum_path.open('xb') as f:
                f.write(checksum_data)
        install(root, archive, version, probe=probe)
    return True


def bootstrap(root, rollback_requested=False):
    if not getattr(sys, 'frozen', False) or sys.platform != 'win32':
        raise ValueError('Bootstrap requires the packaged Windows updater executable')
    ctl = control(root)
    recovery = ctl / 'recovery-updater.exe'
    if not recovery.exists():
        with Path(sys.executable).open('rb') as source, recovery.open('xb') as target:
            shutil.copyfileobj(source, target)
    run = directory(ctl, 'runners') / uuid.uuid4().hex
    run.mkdir(parents=True)
    worker = run / 'PlateUpdater.exe'
    shutil.copy2(sys.executable, worker)
    args = [str(worker), '--root', str(root)]
    if rollback_requested:
        args.append('--rollback')
    subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(r'B:\License Plate Studio'))
    parser.add_argument('--bootstrap', action='store_true')
    parser.add_argument('--rollback', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        print('PASS: Plate Studio updater ' + VERSION)
        return 0
    if sys.platform != 'win32':
        parser.error('Installation requires Windows x64; no files were changed')
    root = args.root.resolve()
    if args.bootstrap:
        bootstrap(root, args.rollback)
        return 0
    ctl = control(root)
    logs = directory(ctl, 'logs')
    log = logs / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8] + '.log')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.StreamHandler(), logging.FileHandler(log, encoding='utf-8')])
    code = 0
    try:
        with update_lock(root):
            if args.rollback:
                rollback(root)
            else:
                update(root)
    except Exception as error:
        LOG.error('%s: %s', type(error).__name__, error)
        code = 1
    LOG.info('Log: %s', log)
    if sys.stdin.isatty():
        input('Press Enter to close. ')
    return code


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as error:
        print('Updater could not start: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
