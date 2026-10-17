import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('github_updater', ROOT / 'tools/github_updater.py')
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


def fixture_package(folder, version, extra=None):
    name = 'License-Plate-Studio-v' + version + '-windows-x64.zip'
    archive = folder / name
    files = {'PlateStudio.exe': b'fake-runtime-' + version.encode(), 'PlateUpdater.exe': b'fake-updater'}
    manifest = {'schemaVersion': 1, 'application': u.PRODUCT, 'version': version,
                'platform': 'windows-x64', 'sourceCommit': 'a' * 40, 'updaterProtocol': 1,
                'files': {n: hashlib.sha256(b).hexdigest() for n, b in files.items()}}
    with zipfile.ZipFile(archive, 'w') as z:
        for n, data in files.items():
            z.writestr('app/' + n, data)
        z.writestr('app/manifest.json', json.dumps(manifest))
        for n in u.ROOT_FILES:
            z.writestr(n, b'fixture-launcher')
        if extra:
            z.writestr(*extra)
    return archive


def release_fixture(archive, version):
    base = 'https://github.com/' + u.REPOSITORY + '/releases/download/v' + version + '/'
    return {'tag_name': 'v' + version, 'draft': False, 'prerelease': False,
            'assets': [{'name': n, 'browser_download_url': base + n}
                       for n in [archive.name, archive.name + '.sha256']]}


class GitHubUpdaterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'License Plate Studio'
        self.root.mkdir()
        self.probe = lambda app: u.verify_app(app)

    def package(self, version, extra=None):
        return fixture_package(self.base, version, extra)

    def install(self, version):
        return u.install(self.root, self.package(version), version, probe=self.probe)

    def data(self):
        for name in ['Projects/original.json','Original Media/photo.jpg','Processed Media/out.png',
                     'Output/export.bin','Presets/custom.json','settings.json','export-preferences.json',
                     'history.json','Build/Source/custom.txt','templates/mine.txt','unknown-user-data.bin',
                     'tools/custom-tool.py','Start Plate.bat']:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'PERSONAL:'+name.encode())
        return {p.relative_to(self.root).as_posix():p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def assert_data(self, original):
        for name,data in original.items():
            self.assertEqual((self.root/name).read_bytes(),data,name)

    def test_install_update_and_rollback_preserve_all_personal_data(self):
        original=self.data();self.install('0.1.2');self.install('0.1.3')
        self.assertEqual(u.verify_app(self.root/'app')['version'],'0.1.3')
        u.rollback(self.root,probe=self.probe)
        self.assertEqual(u.verify_app(self.root/'app')['version'],'0.1.2')
        self.assert_data(original)
        self.assertGreaterEqual(len(list((self.root/'.plate-studio/backups').glob('*/app'))),2)

    def test_post_activation_failure_restores_previous_and_retains_failed_candidate(self):
        self.install('0.1.2');original=self.data()
        def probe(app):
            if app==self.root/'app':raise ValueError('Injected post-activation failure')
            return self.probe(app)
        with self.assertRaisesRegex(ValueError,'Injected'):
            u.install(self.root,self.package('0.1.3'),'0.1.3',probe=probe)
        self.assertEqual(u.verify_app(self.root/'app')['version'],'0.1.2')
        self.assertTrue(list((self.root/'.plate-studio/failed').glob('*/manifest.json')))
        self.assert_data(original)

    def test_staging_probe_failure_does_not_move_existing_app(self):
        self.install('0.1.2')
        with self.assertRaisesRegex(ValueError,'broken runtime'):
            u.install(self.root,self.package('0.1.3'),'0.1.3',probe=lambda _:(_ for _ in ()).throw(ValueError('broken runtime')))
        self.assertEqual(u.verify_app(self.root/'app')['version'],'0.1.2')

    def test_recovery_after_interruption_between_renames(self):
        self.install('0.1.2');txn='b'*32;ctl=u.control(self.root)
        backup=ctl/'backups'/txn/'app';backup.parent.mkdir(parents=True)
        shutil.move(self.root/'app',backup)
        u.atomic_json(ctl/'transaction.json',{'id':txn,'status':'prepared','hadApp':True,'oldVersion':'0.1.2'})
        u.recover(self.root)
        self.assertEqual(u.verify_app(self.root/'app')['version'],'0.1.2')

    def test_power_loss_after_new_app_activation_rolls_back(self):
        self.install('0.1.2');txn='c'*32;ctl=u.control(self.root)
        backup=ctl/'backups'/txn/'app';backup.parent.mkdir(parents=True)
        shutil.move(self.root/'app',backup)
        stage=self.base/'new';u.extract_package(self.package('0.1.3'),stage,'0.1.3')
        shutil.move(stage/'app',self.root/'app')
        u.atomic_json(ctl/'transaction.json',{'id':txn,'status':'prepared','hadApp':True,'oldVersion':'0.1.2'})
        u.recover(self.root)
        self.assertEqual(u.verify_app(self.root/'app')['version'],'0.1.2')

    def test_unmanaged_configuration_inside_app_refuses_update(self):
        self.install('0.1.2');config=self.root/'app/personal.ini';config.write_text('preserve')
        with self.assertRaisesRegex(ValueError,'Unmanaged'):
            self.install('0.1.3')
        self.assertEqual(config.read_text(),'preserve')

    def test_modified_managed_file_refuses_update(self):
        self.install('0.1.2');p=self.root/'app/PlateStudio.exe';p.write_bytes(b'user modification')
        with self.assertRaisesRegex(ValueError,'checksum mismatch'):self.install('0.1.3')
        self.assertEqual(p.read_bytes(),b'user modification')

    def test_bad_zip_paths_and_case_collisions_are_refused(self):
        for name in ['../escape','app/../escape','app/C:evil','app/CON.txt','app/a.','app/PlateStudio.EXE','Projects/mine.json']:
            with self.subTest(name=name),self.assertRaises(ValueError):
                u.extract_package(self.package('0.1.2',(name,b'bad')),self.base/'stage','0.1.2')
        self.assertFalse((self.base/'escape').exists())

    def test_archive_manifest_tamper_refused(self):
        archive=self.package('0.1.2')
        with zipfile.ZipFile(archive) as z:items={n:z.read(n) for n in z.namelist()}
        items['app/PlateStudio.exe']=b'corrupt'
        with zipfile.ZipFile(archive,'w') as z:
            for name,data in items.items():z.writestr(name,data)
        with self.assertRaisesRegex(ValueError,'checksum'):u.extract_package(archive,self.base/'stage','0.1.2')

    def test_version_comparison_is_numeric_and_downgrade_refused(self):
        self.assertGreater(u.version_tuple('0.1.10'),u.version_tuple('0.1.9'))
        self.install('0.1.2')
        for version in ['0.1.2','0.1.1']:
            with self.assertRaises(ValueError):self.install(version)
        for version in ['1.2.3-beta','v1.2.3','01.2.3']:
            with self.assertRaises(ValueError):u.version_tuple(version)

    def test_latest_stable_metadata_requires_both_exact_assets(self):
        a=self.package('0.1.2');release=release_fixture(a,'0.1.2')
        self.assertEqual(u.select_release(release)[0],'0.1.2')
        for changed in [dict(release,prerelease=True),dict(release,draft=True),dict(release,assets=release['assets'][:1])]:
            with self.assertRaises(ValueError):u.select_release(changed)
        release['assets'][0]['browser_download_url']='https://github.com/other/repo/evil.zip'
        with self.assertRaises(ValueError):u.select_release(release)

    def test_download_checksum_install_pipeline_and_already_current(self):
        archive=self.package('0.1.2');release=release_fixture(archive,'0.1.2');requests=[]
        def transport(url,limit,destination=None):
            requests.append(url)
            if url==u.API:return json.dumps(release).encode()
            if url.endswith('.sha256'):return (u.sha256(archive)+'  '+archive.name+'\n').encode()
            self.assertIsNotNone(destination);shutil.copy2(archive,destination);return archive.stat().st_size
        original=self.data()
        self.assertTrue(u.update(self.root,transport=transport,probe=self.probe))
        self.assertFalse(u.update(self.root,transport=transport,probe=self.probe))
        self.assertEqual(len(requests),4)
        self.assertTrue((self.root/'Build'/archive.name).exists());self.assert_data(original)

    def test_bad_download_checksum_leaves_app_and_data_unchanged(self):
        self.install('0.1.2');original=self.data();archive=self.package('0.1.3')
        def transport(url,limit,destination=None):
            if url==u.API:return json.dumps(release_fixture(archive,'0.1.3')).encode()
            if url.endswith('.sha256'):return ('0'*64).encode()
            shutil.copy2(archive,destination)
        with self.assertRaisesRegex(ValueError,'checksum mismatch'):u.update(self.root,transport=transport,probe=self.probe)
        self.assertEqual(u.verify_app(self.root/'app')['version'],'0.1.2');self.assert_data(original)

    def test_network_failure_preserves_working_install(self):
        self.install('0.1.2')
        with self.assertRaises(OSError):u.update(self.root,transport=lambda *a:(_ for _ in ()).throw(OSError('offline')),probe=self.probe)
        self.assertEqual(u.verify_app(self.root/'app')['version'],'0.1.2')

    def test_checksum_parser_and_redirect_host_restrictions(self):
        for content in [b'bad',('a'*64+'  wrong.zip').encode(),('a'*64+'\n'+'b'*64).encode()]:
            with self.assertRaises(ValueError):u.parse_checksum(content,'app.zip')
        for url in ['http://github.com/file','https://evil.test/file','https://github.com@evil.test/file','https://github.com:444/file']:
            with self.assertRaises(ValueError):u.check_url(url)
        self.assertEqual(u.parse_checksum(('a'*64+'  app.zip').encode(),'app.zip'),'a'*64)

    def test_exclusive_lock_is_released_on_exit(self):
        with u.update_lock(self.root):
            with self.assertRaisesRegex(ValueError,'Another updater'):
                with u.update_lock(self.root):pass
        with u.update_lock(self.root):pass

    def test_first_install_failure_keeps_personal_files(self):
        original=self.data()
        def probe(app):
            if app==self.root/'app':raise ValueError('failure')
            return self.probe(app)
        with self.assertRaises(ValueError):u.install(self.root,self.package('0.1.2'),'0.1.2',probe=probe)
        self.assertFalse((self.root/'app').exists());self.assert_data(original)

    def test_failed_rollback_restores_current(self):
        self.install('0.1.2');self.install('0.1.3')
        def probe(app):
            if app==self.root/'app':raise ValueError('rollback failed')
            return self.probe(app)
        with self.assertRaises(ValueError):u.rollback(self.root,probe=probe)
        self.assertEqual(u.verify_app(self.root/'app')['version'],'0.1.3')
