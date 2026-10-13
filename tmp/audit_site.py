from pathlib import Path
from lxml import html
from urllib.parse import urlsplit,unquote
import json,re,subprocess
root=Path(__file__).resolve().parents[1];results=[]
for p in root.glob('*.html'):
 d=html.parse(str(p));ids=d.xpath('//@id');assert len(ids)==len(set(ids)),(p.name,'duplicate IDs')
 assert len(d.xpath('//h1'))==1,(p.name,'h1')
 assert len(d.xpath('//link[@rel="canonical"]'))==1,(p.name,'canonical')
 assert d.xpath('//meta[@name="description"]/@content')[0],p.name
 for a in d.xpath('//a[@href]'):
  href=a.get('href');url=urlsplit(href)
  if url.scheme or url.netloc:continue
  target=root/unquote(url.path) if url.path else p
  if target.suffix=='.html':
   assert target.exists(),(p.name,href)
   if url.fragment:assert html.parse(str(target)).xpath('//*[@id=$id]',id=unquote(url.fragment)),(p.name,href)
 visible=' '.join(d.xpath('//text()[not(ancestor::script) and not(ancestor::style)]'))
 assert not re.search(r'\bERP\b|\bNOC\b|\bSOC\b|digital marketing|managed IT operations|e-commerce',visible,re.I),(p.name,'excluded offerings')
 assert '\u2014' not in visible,(p.name,'em dash')
 assert len(d.xpath('//div[contains(@class,"tp-header-menu")]//details'))==4,p.name
 results.append({'page':p.name,'ids':len(ids),'links':len(d.xpath('//a')),'status':'passed'})
(root/'output/site-audit-static.json').write_text(json.dumps(results,indent=2))
print('PASS: all pages, unique IDs, headings, metadata, local links/anchors, service scope and navigation consistency.')
