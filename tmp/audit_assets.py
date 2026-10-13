from pathlib import Path
from urllib.parse import urlsplit, unquote
import re, json

ROOT = Path(__file__).resolve().parents[1]
seeds = [ROOT / n for n in ('index.html', 'index_4.html', 'projects.html', 'content.html', 'admin/index.html')]
used = set(seeds)
queue = list(seeds)
missing = set()
while queue:
    file = queue.pop()
    if file.suffix not in ('.html', '.css', '.js', '.svg', '.json'):
        continue
    content = file.read_text(encoding='utf-8', errors='replace')
    refs = re.findall(r'''(?:src|href|data-background|data-displacement|content)=["']([^"']+)|url\(\s*["']?([^\s)'";]+)|["'`]((?:\.?\.?/)*assets/[^"'`\s]+|\.\.?/[^"'`\s]+\.(?:json|webp|png|svg|jpg|woff2))["'`]''', content)
    for groups in refs:
        ref = next(x for x in groups if x)
        if ref.startswith('https://tekscaleup.com/assets/'):
            ref = urlsplit(ref).path
        if ref.startswith(('http:', 'https:', 'data:', '#', 'mailto:', 'tel:')) or '${' in ref:
            continue
        if not re.search(r'\.(?:css|js|html|json|webp|png|jpg|jpeg|gif|svg|woff2?|ttf|ico)(?:[?#]|$)', ref):
            continue
        ref = unquote(urlsplit(ref).path)
        target = ((ROOT / ref.lstrip('/')) if ref.startswith(('/', 'assets/')) else file.parent / ref).resolve()
        if not target.is_relative_to(ROOT):
            continue
        if target.is_file():
            if target not in used:
                used.add(target)
                queue.append(target)
        else:
            missing.add(str(target.relative_to(ROOT)))

assets = set((ROOT/'assets').rglob('*'))
assets = {p for p in assets if p.is_file() and 'qa' not in p.parts and 'originals' not in p.parts}
licenses = {p for p in assets if p.suffix == '.txt'}
used |= licenses
unused = sorted(assets - used)
report = {'used': sorted(str(p.relative_to(ROOT)).replace('\\','/') for p in used),
          'unused': [str(p.relative_to(ROOT)).replace('\\','/') for p in unused],
          'missing': sorted(missing),
          'unused_bytes': sum(p.stat().st_size for p in unused)}
(ROOT/'tmp/asset-audit.json').write_text(json.dumps(report, indent=2),encoding='utf-8')
print(json.dumps({**report, 'used': len(used)}, indent=2))
