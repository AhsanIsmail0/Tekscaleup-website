"""Create a deployable folder containing only reachable runtime files."""
from pathlib import Path
import json, shutil, subprocess, sys
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root/'tmp/verify_template.py')], check=True, cwd=root)
subprocess.run([sys.executable, str(root/'tmp/audit_assets.py')], check=True, cwd=root, stdout=subprocess.DEVNULL)
audit = json.loads((root/'tmp/asset-audit.json').read_text())
assert not audit['missing'], audit['missing']
destination = root/'dist'
if destination.exists():
    assert destination.resolve() == root/'dist'
    shutil.rmtree(destination)
destination.mkdir()
for relative in audit['used']:
    target = destination/relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root/relative, target)
archive = root/'output/tekscaleup-deployment.zip'
archive.parent.mkdir(exist_ok=True)
with ZipFile(archive, 'w', ZIP_DEFLATED) as z:
    for p in sorted(destination.rglob('*')):
        if p.is_file():
            z.write(p, p.relative_to(destination).as_posix())
print(f'Deployment folder: {destination}')
print(f'Deployment ZIP: {archive} ({archive.stat().st_size:,} bytes)')
