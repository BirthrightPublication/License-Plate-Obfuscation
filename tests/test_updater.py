import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from updater import install, rollback, find_release

class UpdaterTests(unittest.TestCase):
    def bundle(self, folder, version, corrupt=False, unsafe=False):
        path = folder / (version+'.zip')
        name = '../escape' if unsafe else 'index.html'
        data = version.encode()
        digest = 'bad' if corrupt else hashlib.sha256(data).hexdigest()
        with zipfile.ZipFile(path,'w') as z:
            z.writestr(name,data)
            z.writestr('release.json',json.dumps({'version':version,'files':{name:digest}}))
        return path
    def test_update_rollback_preserves_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); root=p/'Installed';root.mkdir();(root/'projects.json').write_text('keep')
            install(self.bundle(p,'0.1.0'),root)
            self.assertEqual(json.loads((root/'versions/0.1.0/release.json').read_text())['version'],'0.1.0')
            install(self.bundle(p,'0.1.1'),root)
            rollback(root)
            self.assertEqual(json.loads((root/'current.json').read_text())['current'],'0.1.0')
            self.assertEqual((root/'projects.json').read_text(),'keep')
    def test_corrupt_or_unsafe_release_does_not_activate(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);root=p/'Installed'
            for version, corrupt, unsafe in [('0.1.0',True,False),('0.1.1',False,True)]:
                with self.assertRaises(ValueError):install(self.bundle(p,version,corrupt,unsafe),root)
            self.assertFalse((root/'current.json').exists())
    def test_repeat_install_preserves_existing_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);a=self.bundle(p,'0.1.0');root=p/'Installed';install(a,root)
            with self.assertRaises(ValueError):install(a,root)
            self.assertEqual((root/'versions/0.1.0/index.html').read_text(),'0.1.0')
    def test_failed_update_keeps_current_and_prior_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);root=p/'Installed';install(self.bundle(p,'0.1.0'),root)
            pointer=(root/'current.json').read_bytes()
            with self.assertRaises(ValueError):install(self.bundle(p,'0.1.1',corrupt=True),root)
            self.assertEqual((root/'current.json').read_bytes(),pointer)
            self.assertEqual((root/'versions/0.1.0/index.html').read_text(),'0.1.0')
    def test_patch_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);archive=p/'patch.zip'
            with zipfile.ZipFile(archive,'w') as z:
                z.writestr('release.json',json.dumps({'version':'0.1.1','kind':'patch','files':{}}))
            with self.assertRaisesRegex(ValueError,'patches are refused'):install(archive,p/'Installed')
    def test_build_discovery_ignores_unrelated_packages(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            for version, app in [('0.1.1','birthright.license-plate-studio'),('9.9.9','other')]:
                with zipfile.ZipFile(p/(version+'.zip'),'w') as z:
                    z.writestr('release.json',json.dumps({'version':version,'application':app,'kind':'full'}))
            self.assertEqual(find_release(p).name,'0.1.1.zip')
