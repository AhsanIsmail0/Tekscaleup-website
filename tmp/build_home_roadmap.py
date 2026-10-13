from pathlib import Path
from lxml import html,etree

def build(ROOT):
 steps=[('Discover','Understand your goals, users, current setup and the challenge to solve.'),('Plan','Agree the priorities, scope, approach and delivery plan.'),('Design','Explore user journeys, interfaces and prototypes before development.'),('Build','Turn the agreed solution into working technology, with regular progress reviews.'),('Test','Check the agreed functionality and experience, and address issues before release.'),('Launch','Prepare the release and handover, then agree the next improvements.')]
 section=html.fromstring('''<section class="ts-roadmap" id="process" aria-labelledby="ts-roadmap-title"><div class="container container-1750"><div class="ts-roadmap-header"><div><span class="tp-section-subtitle">How we work</span><h2 id="ts-roadmap-title">From first idea.<br><span>To what comes next.</span></h2></div><p>A clear path from understanding the challenge to delivering the solution. Scroll to follow the process.</p></div><div class="ts-roadmap-journey"><svg class="ts-roadmap-line" viewBox="0 0 1200 360" fill="none" aria-hidden="true"><path class="ts-roadmap-track" d="M 65 235 C 130 330 210 330 280 235 S 410 100 495 180 S 620 295 710 175 S 830 50 925 115 S 1060 210 1135 65"/><path class="ts-roadmap-progress" d="M 65 235 C 130 330 210 330 280 235 S 410 100 495 180 S 620 295 710 175 S 830 50 925 115 S 1060 210 1135 65"/><g class="ts-roadmap-nodes"></g><circle class="ts-roadmap-marker-halo" r="22" cx="65" cy="235"/><circle class="ts-roadmap-marker" r="9" cx="65" cy="235"/></svg><ol class="ts-roadmap-steps"></ol></div><div class="ts-roadmap-caption"><span>One connected team. Every step of the way.</span><span data-roadmap-count>01 / 06</span></div></div></section>''')
 nodes=section.xpath('.//*[local-name()="g"]')[0];listing=section.xpath('.//ol')[0]
 for i,((title,copy),(x,y)) in enumerate(zip(steps,[(65,235),(280,235),(495,180),(710,175),(925,115),(1135,65)])):
  nodes.append(etree.Element('circle',cx=str(x),cy=str(y),r='7',attrib={'data-roadmap-node':str(i)}))
  listing.append(html.fromstring(f'<li data-roadmap-step="{i}"><span class="ts-roadmap-number">0{i+1}</span><h3>{title}</h3><p>{copy}</p></li>'))
 for file in ['index.html','index_4.html']:
  p=ROOT/file;doc=html.parse(str(p)).getroot();old=doc.xpath('//*[@id="process"]')[0];old.getparent().replace(old,html.fromstring(html.tostring(section)))
  doc.xpath('//head')[0].append(etree.Element('link',rel='stylesheet',href='assets/css/process-roadmap.css?v=20261013'))
  doc.xpath('//body')[0].append(etree.Element('script',src='assets/js/process-roadmap.js?v=20261013'))
  p.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode'),encoding='utf-8')

