"""Serve only the packaged UI locally; supports Python and a Windows frozen build."""
import argparse
import hashlib
import http.server
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import webbrowser

ASSETS = {
    'index.html': 'text/html; charset=utf-8',
    'src/app.js': 'text/javascript; charset=utf-8',
    'src/domain.js': 'text/javascript; charset=utf-8',
    'src/style.css': 'text/css; charset=utf-8',
}


def application_root():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    root = Path(__file__).resolve().parent.parent
    pointer = root / 'Installed/current.json'
    if pointer.exists():
        version = json.loads(pointer.read_text(encoding='utf-8'))['current']
        if not isinstance(version, str) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
            raise ValueError('Invalid installed version pointer')
        return root / 'Installed/versions' / version
    return root


def verify_assets(root):
    manifest = json.loads((root / 'release.json').read_text(encoding='utf-8'))
    if not re.fullmatch(r'\d+\.\d+\.\d+', manifest.get('version', '')):
        raise ValueError('Unsupported application version')
    for name in ASSETS:
        expected = manifest['files'][name]
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Damaged application file: ' + name)
    return manifest


def make_server(root, port=4173):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.respond(False)

        def do_HEAD(self):
            self.respond(True)

        def respond(self, head):
            name = unquote(urlsplit(self.path).path).lstrip('/') or 'index.html'
            if name == 'favicon.ico':
                self.send_response(204)
                self.end_headers()
                return
            if name not in ASSETS:
                self.send_error(404)
                return
            data = (root / name).read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', ASSETS[name])
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            if not head:
                self.wfile.write(data)

        def log_message(self, *args):
            pass

    return http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--port', type=int, default=4173)
    parser.add_argument('--app-root', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        root = args.app_root or application_root()
        manifest = verify_assets(root)
        if args.check:
            print('PASS: v' + manifest['version'] + ' application assets verified.', flush=True)
            return 0
        with make_server(root, args.port) as server:
            url = 'http://localhost:' + str(server.server_port)
            print('License Plate Obfuscation Studio v' + manifest['version'], flush=True)
            print('READY ' + url, flush=True)
            print('Keep this window open. Press Ctrl+C here to stop.', flush=True)
            print('Use the same browser profile and localhost:4173 to retain local data.', flush=True)
            if not args.no_browser and not webbrowser.open(url):
                print('Open your browser and enter the address shown above.', flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        return 0
    except (OSError, ValueError, KeyError) as error:
        print('Cannot start: ' + str(error), file=sys.stderr)
        print('If port 4173 is occupied, close the previous Studio server. '
              'Do not change the port for existing saved projects.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
