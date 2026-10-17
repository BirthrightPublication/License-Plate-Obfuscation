import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
with patch.object(sys, 'path', [str(ROOT / 'tools'), *sys.path]):
    spec = importlib.util.spec_from_file_location('windows_entry', ROOT / 'tools/windows_entry.py')
    entry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(entry)


class WindowsEntryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='Plate Entry Test ')
        self.addCleanup(self.tmp.cleanup)
        # Windows may return an 8.3 TEMP alias; dispatch intentionally canonicalizes it.
        self.root = (Path(self.tmp.name) / 'Source and Installation').resolve()
        self.root.mkdir()
        self.commands = []

    def record(self, command, cwd):
        self.commands.append((command, cwd))
        return 17

    def source(self):
        tools = self.root / 'tools'
        tools.mkdir(exist_ok=True)
        for filename in ['launch.py', 'github_updater.py']:
            (tools / filename).write_text('# source marker', encoding='utf-8')

    def native(self):
        app = self.root / 'app'
        app.mkdir()
        files = {'PlateStudio.exe': b'fixture application', 'PlateUpdater.exe': b'fixture updater'}
        for name, content in files.items():
            (app / name).write_bytes(content)
        (app / 'manifest.json').write_text(json.dumps({
            'schemaVersion': 1, 'application': 'birthright.license-plate-studio',
            'version': '0.1.2', 'platform': 'windows-x64', 'sourceCommit': 'a' * 40,
            'updaterProtocol': 1,
            'files': {name: hashlib.sha256(content).hexdigest() for name, content in files.items()},
        }), encoding='utf-8')
        return app

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file()}

    def test_source_start_retains_launch_arguments_legacy_selection_and_exit_code(self):
        self.source()
        pointer = self.root / 'Installed/current.json'
        pointer.parent.mkdir()
        pointer.write_text('{"current":"0.1.1"}', encoding='utf-8')
        before = self.snapshot()
        self.assertEqual(entry.dispatch(self.root, 'start', ['--no-browser', '--port', '4173'], self.record), 17)
        self.assertEqual(self.commands, [([sys.executable, str(self.root / 'tools/launch.py'),
                                          '--no-browser', '--port', '4173'], self.root)])
        self.assertEqual(self.snapshot(), before)

    def test_native_is_preferred_over_source_and_verified_before_dispatch(self):
        self.source()
        app = self.native()
        self.assertEqual(entry.dispatch(self.root, 'start', ['--check'], self.record), 17)
        self.assertEqual(self.commands, [([str(app / 'PlateStudio.exe'), '--check'], self.root)])
        (app / 'PlateStudio.exe').write_bytes(b'modified file')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            entry.dispatch(self.root, 'start', runner=self.record)
        self.assertEqual(len(self.commands), 1)

    def test_damaged_native_never_falls_back_to_source_or_changes_personal_files(self):
        self.source()
        app = self.native()
        (app / 'PlateStudio.exe').unlink()
        (self.root / 'Projects').mkdir()
        (self.root / 'Projects/keep.json').write_bytes(b'personal project')
        (self.root / 'settings.json').write_bytes(b'personal settings')
        before = self.snapshot()
        for action in ['start', 'update']:
            with self.subTest(action=action), self.assertRaises(ValueError):
                entry.dispatch(self.root, action, runner=self.record)
        self.assertEqual(self.commands, [])
        self.assertEqual(self.snapshot(), before)

    def test_invalid_native_manifest_and_unknown_app_file_are_refused(self):
        app = self.native()
        (app / 'private-settings.ini').write_text('preserve', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unmanaged'):
            entry.dispatch(self.root, 'update', runner=self.record)
        (app / 'private-settings.ini').unlink()
        (app / 'manifest.json').write_text('not json', encoding='utf-8')
        with self.assertRaises(ValueError):
            entry.dispatch(self.root, 'start', runner=self.record)
        self.assertEqual(self.commands, [])

    def test_native_update_check_never_bootstraps_and_normal_update_uses_detached_worker(self):
        app = self.native()
        self.assertEqual(entry.dispatch(self.root, 'update', ['--check'], self.record), 17)
        self.assertEqual(entry.dispatch(self.root, 'update', runner=self.record), 17)
        self.assertEqual(self.commands, [
            ([str(app / 'PlateUpdater.exe'), '--check'], self.root),
            ([str(app / 'PlateUpdater.exe'), '--bootstrap', '--root', str(self.root)], self.root),
        ])

    def test_recovery_marker_blocks_source_start_and_selects_recovery_for_update(self):
        self.source()
        control = self.root / '.plate-studio'
        control.mkdir()
        recovery = control / 'recovery-updater.exe'
        recovery.write_bytes(b'fixture recovery')
        with self.assertRaisesRegex(ValueError, 'Native application is missing'):
            entry.dispatch(self.root, 'start', runner=self.record)
        self.assertEqual(entry.dispatch(self.root, 'update', ['--check'], self.record), 17)
        self.assertEqual(self.commands, [([str(recovery), '--check'], self.root)])

    def test_journal_without_recovery_blocks_start_and_update_without_changes(self):
        self.source()
        control = self.root / '.plate-studio'
        control.mkdir()
        (control / 'transaction.json').write_text('{"id":"preserved"}', encoding='utf-8')
        before = self.snapshot()
        for action in ['start', 'update']:
            with self.subTest(action=action), self.assertRaises(ValueError):
                entry.dispatch(self.root, action, runner=self.record)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.commands, [])

    def test_source_update_requires_explicit_confirmation_before_starting_any_worker(self):
        self.source()
        before = self.snapshot()
        self.assertEqual(entry.dispatch(self.root, 'update', runner=self.record, confirm=lambda _: 'no'), 2)
        self.assertEqual(self.commands, [])
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(entry.dispatch(self.root, 'update', runner=self.record, confirm=lambda _: 'INSTALL'), 17)
        self.assertEqual(self.commands, [([sys.executable, str(self.root / 'tools/github_updater.py'),
                                          '--root', str(self.root)], self.root)])
        self.assertNotIn('--bootstrap', self.commands[0][0])

    def test_source_check_never_prompts_and_update_arguments_cannot_override_root(self):
        self.source()
        def forbidden(_):
            raise AssertionError('Check must never request installation confirmation')
        before = self.snapshot()
        self.assertEqual(entry.dispatch(self.root, 'update', ['--check'], self.record, forbidden), 17)
        self.assertEqual(self.commands[0][0], [sys.executable, str(self.root / 'tools/github_updater.py'), '--check'])
        for arguments in [['--root', 'other'], ['--bootstrap'], ['--check', '--rollback']]:
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                entry.dispatch(self.root, 'update', arguments, self.record)
        self.assertEqual(self.snapshot(), before)

    def test_real_source_diagnostics_do_not_write_to_selected_source_folder(self):
        shutil.copytree(ROOT / 'tools', self.root / 'tools', ignore=shutil.ignore_patterns('__pycache__'))
        before = self.snapshot()
        result = subprocess.run([sys.executable, str(self.root / 'tools/windows_entry.py'),
                                 '--root', str(self.root), 'update', '--', '--check'],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('SOURCE UPDATER CHECK', result.stdout)
        self.assertEqual(self.snapshot(), before)

    @unittest.skipUnless(sys.platform == 'win32', 'Actual cmd.exe execution requires Windows')
    def test_windows_primary_and_alias_batches_dispatch_checks_and_forward_failure_codes(self):
        shutil.copytree(ROOT / 'tools', self.root / 'tools', ignore=shutil.ignore_patterns('__pycache__'))
        for filename in ['Start Plate.bat', 'START APPLICATION.bat', 'Update Plate.bat', 'UPDATE APPLICATION.bat']:
            shutil.copy2(ROOT / filename, self.root / filename)
        # Child fixtures permit a real cmd/Python argument and status check without launching a browser or updater.
        (self.root / 'tools/launch.py').write_text('import sys\nprint(repr(sys.argv[1:]))\nsys.exit(23)\n', encoding='utf-8')
        before = self.snapshot()
        for filename, expected in [('Start Plate.bat', 23), ('START APPLICATION.bat', 23),
                                   ('Update Plate.bat', 0), ('UPDATE APPLICATION.bat', 0)]:
            with self.subTest(filename=filename):
                result = subprocess.run('call "' + str(self.root / filename) + '" --check', shell=True,
                                        cwd=self.root.parent, capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                if expected == 23:
                    self.assertIn("['--check']", result.stdout)
        self.assertEqual(self.snapshot(), before)


if __name__ == '__main__':
    unittest.main()
