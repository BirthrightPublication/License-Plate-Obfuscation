"""Dispatch the Windows source launchers without installing or migrating on start."""
import argparse
from pathlib import Path
import subprocess
import sys

# In particular, --check must not create a bytecode cache in a source checkout.
if __name__ == '__main__':
    sys.dont_write_bytecode = True
from github_updater import verify_app


def invoke(command, root):
    return subprocess.run(command, cwd=root).returncode


def dispatch(root, action, arguments=(), runner=None, confirm=None):
    root = Path(root).resolve()
    arguments = list(arguments)
    runner = runner or invoke
    confirm = confirm or input
    if action not in ('start', 'update'):
        raise ValueError('Unknown launcher action')
    if action == 'update' and arguments not in ([], ['--check']):
        raise ValueError('Update supports only --check or no arguments; use Rollback Plate.bat for rollback')

    app = root / 'app'
    recovery = root / '.plate-studio/recovery-updater.exe'
    journal = root / '.plate-studio/transaction.json'
    if app.exists() or app.is_symlink():
        # Never hide a damaged/mixed native installation by silently serving source.
        verify_app(app)
        if action == 'start':
            return runner([str(app / 'PlateStudio.exe'), *arguments], root)
        command = [str(app / 'PlateUpdater.exe')]
        command += ['--check'] if arguments else ['--bootstrap', '--root', str(root)]
        return runner(command, root)

    if recovery.exists() or journal.exists():
        if action == 'start':
            raise ValueError('Native application is missing; use Update Plate.bat to recover. Source was not started.')
        if not recovery.is_file():
            raise ValueError('Interrupted installation has no recovery updater. Preserve this folder and obtain the complete installation ZIP.')
        command = [str(recovery)]
        command += ['--check'] if arguments else ['--bootstrap', '--root', str(root)]
        return runner(command, root)

    script = root / 'tools' / ('launch.py' if action == 'start' else 'github_updater.py')
    if not script.is_file():
        raise ValueError('No complete native installation or source launcher found. Extract the complete Windows installation ZIP into a new folder; do not replace projects or settings.')
    if action == 'start':
        print('SOURCE PROTOTYPE: experimental browser/CSS preview; True Engine is NOT integrated.', flush=True)
        print('Keeping the existing browser profile, localhost:4173 and legacy Installed selection.', flush=True)
        return runner([sys.executable, str(script), *arguments], root)
    if arguments:
        print('SOURCE UPDATER CHECK: no network request, installation, or migration.', flush=True)
        return runner([sys.executable, str(script), '--check'], root)

    print('This is a source/development folder, not an installed Windows application.', flush=True)
    print('The GitHub updater would install the latest published Windows package under:', root / 'app', flush=True)
    print('Existing source, projects, settings, legacy Installed versions and root files will be preserved.', flush=True)
    print('This does not build or integrate True Engine. --check performs diagnostics only.', flush=True)
    try:
        answer = confirm('Type INSTALL to authorize this installation in the folder shown above: ')
    except EOFError:
        answer = ''
    if answer.strip() != 'INSTALL':
        print('Cancelled. No updater was started and no files were changed.', flush=True)
        return 2
    # The source worker lives outside app/, so no frozen-executable bootstrap is needed.
    return runner([sys.executable, str(script), '--root', str(root)], root)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('action', choices=['start', 'update'])
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    forwarded = args.arguments[1:] if args.arguments[:1] == ['--'] else args.arguments
    try:
        return dispatch(args.root, args.action, forwarded)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print('Cannot ' + args.action + ': ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
