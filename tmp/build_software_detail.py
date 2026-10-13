from copy import deepcopy
from lxml import html, etree

def build(doc, work, ROOT, cls, text, content):
    page=deepcopy(doc)
    main=page.xpath('//main')[0]
    for child in list(main): main.remove(child)
    page.xpath('//body')[0].set('class',page.xpath('//body')[0].get('class','')+' ts-software-detail')
    for section in html.fragments_fromstring((ROOT/'tmp/software-development-content.html').read_text(encoding='utf-8')):
        main.append(section)
    button=deepcopy(cls('tp-header-btn-box',page)[0].xpath('./a')[0])
    for node in button.xpath('.//*[@id]'):
        old=node.get('id'); node.set('id','detail-hero-button')
        for target in button.iter():
            for attr,value in list(target.attrib.items()):
                if attr!='id': target.set(attr,value.replace(old,'detail-hero-button'))
    text(cls('tp-btn-black-text',button)[0],'Discuss your software project')
    button.set('href','#contact')
    main.xpath('.//*[@data-detail-button]')[0].append(button)
    process=deepcopy(work)
    main.insert(3,process)
    for a in page.xpath('//a[@href]'):
        href=a.get('href')
        if href=='#top': a.set('href','index.html')
        elif href.startswith('#') and href not in ('#contact','#capabilities','#process','#capability-1','#capability-2','#capability-3','#capability-4'):
            a.set('href','index.html'+href)
    text(page.xpath('//title')[0],'Startup & Scaleup Services | TekScaleUp')
    desc='Web development, mobile app development, design audits and code audits. Explore TekScaleUp startup and scaleup services.'
    for node in page.xpath('//meta[@name="description"] | //meta[@property="og:description"]'): node.set('content',desc)
    for node in page.xpath('//meta[@property="og:title"]'): node.set('content','Startup & Scaleup Services | TekScaleUp')
    for node in page.xpath('//meta[@property="og:url"]'): node.set('content','https://tekscaleup.com/software-development.html')
    for node in page.xpath('//link[@rel="canonical"]'): node.set('href','https://tekscaleup.com/software-development.html')
    page.xpath('//head')[0].append(etree.Element('link',rel='stylesheet',href='assets/css/software-detail.css?v=20261013'))
    page.xpath('//body')[0].append(etree.Element('script',src='assets/js/software-detail.js?v=20261013'))
    text(page.xpath('//*[@id="ts-enquiry-title"]')[0],'Tell us about your software project.')
    (ROOT/'software-development.html').write_text('<!doctype html>\n'+html.tostring(page,encoding='unicode',method='html'),encoding='utf-8')
