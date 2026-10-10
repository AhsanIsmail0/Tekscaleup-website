from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parent.parent

class PreviewHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        target = (ROOT / path.lstrip('/')).resolve()
        allowed = target in (ROOT, ROOT / 'index.html', ROOT / 'index_4.html') or (ROOT / 'assets') in target.parents
        if not allowed or (target.is_dir() and target != ROOT):
            self.send_error(404)
            return
        super().do_GET()

    def log_message(self, *args):
        pass

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
print(f'TekScaleUp preview: http://127.0.0.1:{port}', flush=True)
ThreadingHTTPServer(('127.0.0.1', port), PreviewHandler).serve_forever()
