"""Package static assets plus a compiled Pages Worker for dashboard upload."""
from pathlib import Path
import subprocess, sys, shutil
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, 'tmp/package_site.py'], cwd=root, check=True)
subprocess.run(['npx.cmd', '--yes', 'wrangler@4.150.0', 'pages', 'functions', 'build',
                'functions', '--outdir', 'tmp/dashboard-worker',
                '--compatibility-date', '2026-10-13', '--minify'], cwd=root, check=True)
worker = root/'tmp/dashboard-worker/index.js'
assert worker.is_file()
assert not worker.read_bytes().startswith(b'------formdata'), 'Dashboard requires JavaScript, not multipart upload data'
shutil.copy2(worker, root/'dist/_worker.js')
archive = root/'output/tekscaleup-cloudflare.zip'
with ZipFile(archive, 'w', ZIP_DEFLATED) as bundle:
    for file in sorted((root/'dist').rglob('*')):
        if file.is_file():
            bundle.write(file, file.relative_to(root/'dist').as_posix())
with ZipFile(archive) as bundle:
    assert '_worker.js' in bundle.namelist()
print(f'Cloudflare dashboard bundle: {archive} ({archive.stat().st_size:,} bytes)')
