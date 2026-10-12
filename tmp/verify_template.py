from pathlib import Path
from lxml import html

root = Path(__file__).resolve().parents[1]
original = html.fromstring((root/'tmp/index_4.before-content.html').read_text(encoding='utf-8'))
page = html.fromstring((root/'index.html').read_text(encoding='utf-8'))
def nodes(doc, name):
    return doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," '+name+' ")]')
for name in ['tp-char-animation','tp-service-panel','tp-panel-pin','tp-work-item','tp-testimonial-item','tp-text-slide-active']:
    assert len(nodes(page,name)) == len(nodes(original,name)), name
for name in ['tp-btn-black','tp-btn-black-filter','tp-btn-black-circle']:
    assert len(nodes(page,name)) == len(nodes(original,name)) + 5, name
for ident in ['smooth-wrapper','smooth-content','magic-cursor']:
    assert page.xpath(f'//*[@id="{ident}"]'), ident
for name in ['plugin.js','main.js','slider-active.js','tp-cursor.js','webgl.js','portfolio-slider-1.js']:
    assert any(p.split('?')[0] == f'assets/js/{name}' for p in page.xpath('//script/@src')), name
missing = [p for p in page.xpath('//@src | //@data-background | //@data-displacement') if p.startswith('assets/') and not (root/p.split('?')[0]).is_file()]
assert not missing, missing
ids = page.xpath('//@id')
assert len(ids) == len(set(ids)), 'Duplicate IDs'
for href in page.xpath('//a/@href'):
    if href.startswith('#') and len(href)>1:
        assert href[1:] in ids, href
assert len(nodes(page,'tp-project-item')) == 3
assert not nodes(page, 'tp-funfact-area')
assert not nodes(page, 'tp-funfact-panel')
assert not nodes(page, 'ts-hero-proof')
assert nodes(page, 'ts-hero-system')
assert page.xpath('//img[@alt="Canada flag"]')
assert page.xpath('//i[@data-purecounter-end]/@data-purecounter-end') == ['20', '100', '100', '200']
assert page.xpath('//a[@href="projects.html"]')
portfolio = html.fromstring((root/'projects.html').read_text(encoding='utf-8'))
assert len(nodes(portfolio,'tp-project-item')) == 8
assert len(portfolio.xpath('//h1')) == 1
for target in (page, portfolio):
    identifiers = target.xpath('//@id')
    assert len(identifiers) == len(set(identifiers)), 'Duplicate IDs'
    for href in target.xpath('//a/@href'):
        if href.startswith('#') and len(href)>1:
            assert href[1:] in identifiers, href
    missing = [p for p in target.xpath('//@src | //@data-background | //@data-displacement') if p.startswith('assets/') and not (root/p.split('?')[0]).is_file()]
    assert not missing, missing
    assert '\u2014' not in html.tostring(target, encoding='unicode'), 'Em dash'
assert not nodes(page,'tp-video-area')
assert len(nodes(page,'tp-award-item')) == 4
assert 'avron@solution.com' not in page.text_content()
assert 'Clutch' not in page.text_content()
assert (root/'index.html').read_bytes() == (root/'index_4.html').read_bytes()
print('Passed: retained GSAP hooks, sliders and buttons; removed network; 4 verified counters; 3 featured and 8 portfolio projects; local assets and anchors on both pages.')
