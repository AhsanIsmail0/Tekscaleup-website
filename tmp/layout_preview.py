"""Serve a packaged site with a public CMS snapshot, including delayed responses."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlsplit
import argparse, json, time

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('port', type=int)
parser.add_argument('--delay', type=float, default=0)
parser.add_argument('--directory', default='dist')
args = parser.parse_args()
fixture = root/'output/live-content-audit-20261014.json'
if fixture.exists():
    content = fixture.read_bytes()
else:
    seed = json.loads((root/'admin/seed.json').read_text(encoding='utf-8'))
    content = json.dumps({'items':[{**item,'version':1} for item in seed],
                          'routes':[{'page':item['page'],'published':True} for item in seed if item.get('page')]}).encode()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *values, **kw):
        super().__init__(*values, directory=str(root/args.directory), **kw)
    def do_GET(self):
        if urlsplit(self.path).path == '/api/content':
            time.sleep(args.delay)
            self.send_response(200)
            self.send_header('Content-Type','application/json')
            self.send_header('Cache-Control','no-store')
            self.send_header('Content-Length',str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        elif urlsplit(self.path).path.startswith('/api/'):
            self.send_error(404)
        else:
            super().do_GET()
    def log_message(self, *values):
        pass

print(f'Packaged layout preview: http://127.0.0.1:{args.port}, CMS delay {args.delay}s', flush=True)
ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
