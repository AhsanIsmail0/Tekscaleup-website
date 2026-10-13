from pathlib import Path
from copy import deepcopy
from lxml import html,etree

def build(ROOT):
 template=html.parse(str(ROOT/'careers.html')).getroot();main=template.xpath('//main')[0]
 for child in list(main):main.remove(child)
 main.append(html.fromstring('<article id="cms-content"><h1>Loading content…</h1><p>If this message remains, the content service is unavailable. <a href="index.html">Return to the homepage</a>.</p></article>'))
 template.xpath('//title')[0].text='Content | TekScaleUp'
 (ROOT/'content.html').write_text('<!doctype html>\n'+html.tostring(template,encoding='unicode'),encoding='utf-8')
 for p in ROOT.glob('*.html'):
  doc=html.parse(str(p)).getroot();doc.xpath('//head')[0].append(etree.Element('link',rel='stylesheet',href='assets/css/cms-public.css'))
  doc.xpath('//body')[0].append(etree.Element('script',src='assets/js/cms-public.js'))
  p.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode'),encoding='utf-8')
