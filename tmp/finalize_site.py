from pathlib import Path
from lxml import html,etree
from PIL import Image

def build(ROOT):
 for p in ROOT.glob('*.html'):
  doc=html.parse(str(p)).getroot();head=doc.xpath('//head')[0]
  canonical=doc.xpath('//link[@rel="canonical"]')
  url='https://tekscaleup.com/'+('' if p.name in ['index.html','index_4.html'] else p.name)
  if canonical:canonical[0].set('href',url)
  else:head.append(etree.Element('link',rel='canonical',href=url))
  for node in doc.xpath('//link[@href] | //script[@src]'):
   attr='src' if node.tag=='script' else 'href'
   value=node.get(attr)
   if value.startswith('assets/') and value.split('?')[0].endswith(('.css','.js')):node.set(attr,value.split('?')[0]+'?v=layout-20261014-1')
  title=doc.xpath('//title')[0].text_content()
  for meta in doc.xpath('//meta[@property="og:title"]'):meta.set('content',title)
  for image in doc.xpath('//img[@src]'):
   asset=ROOT/image.get('src').split('?')[0]
   if asset.exists() and asset.suffix.lower() in ['.png','.webp','.jpg','.jpeg']:
    with Image.open(asset) as im:w,h=im.size
    image.set('width',str(w));image.set('height',str(h));image.set('decoding','async')
  p.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode'),encoding='utf-8')

