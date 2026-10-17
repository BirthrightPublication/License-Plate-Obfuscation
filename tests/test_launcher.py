import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('studio_launcher', ROOT / 'tools/launch.py')
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LauncherTests(unittest.TestCase):
    def test_assets_checked_and_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = {}
            for name in launcher.ASSETS:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b'test asset')
                files[name] = hashlib.sha256(p.read_bytes()).hexdigest()
            manifest = root / 'release.json'
            manifest.write_text(json.dumps({'version': '0.1.1', 'files': files}))
            self.assertEqual(launcher.verify_assets(root)['version'], '0.1.1')
            (root / 'src/app.js').write_bytes(b'damaged')
            with self.assertRaisesRegex(ValueError, 'Damaged application file'):
                launcher.verify_assets(root)

    def test_http_only_exposes_assets_with_module_mime_types(self):
        server = launcher.make_server(ROOT, 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = 'http://127.0.0.1:' + str(server.server_port)
            self.assertEqual(server.server_address[0], '127.0.0.1')
            for name, mime in launcher.ASSETS.items():
                with urllib.request.urlopen(base + '/' + name) as response:
                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.headers['Content-Type'], mime)
                    self.assertEqual(response.read(), (ROOT / name).read_bytes())
            for path in ['/tools/updater.py', '/projects.json', '/../README.md', '/src/', '/%2e%2e/README.md']:
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(base + path)
                self.assertEqual(error.exception.code, 404)
        finally:
            server.shutdown()
            thread.join()
            server.server_close()

    def test_conflicting_port_does_not_replace_server(self):
        server = launcher.make_server(ROOT, 0)
        try:
            with self.assertRaises(OSError):
                launcher.make_server(ROOT, server.server_port)
        finally:
            server.server_close()
