"""Build the global services page from the shared, original template components."""
from copy import deepcopy
from lxml import html, etree

def build(doc, services, projects, work, ROOT, cls, text, content):
    page = deepcopy(doc)
    main = page.xpath('//main')[0]
    for child in list(main):
        main.remove(child)
    page.xpath('//body')[0].set('class', page.xpath('//body')[0].get('class','')+' ts-services-page')
    main.append(html.fromstring('''<section class="ts-services-hero"><div class="container container-1750">
      <span class="tp-section-subtitle">Our expertise</span>
      <div class="ts-services-heading"><h1 class="tp-char-animation">Services &amp;<br>capabilities.</h1><img src="assets/img/logo/tekscaleup-icon.svg" alt="" aria-hidden="true"></div>
      <div class="ts-services-hero-meta"><p>Build digital products. Strengthen your operations.<br>Develop your next product with one connected team.</p><span>Pakistan · Canada · Japan</span><a href="#services">Scroll to explore ↓</a></div>
    </div></section>'''))
    # A code-native brand visual replaces the reference's unrelated stock photograph.
    main.append(html.fromstring('''<section class="ts-services-brand" aria-label="Connected technology, design and AI">
      <div class="ts-services-brand-grid" aria-hidden="true"></div><span class="ts-services-brand-label">ONE CONNECTED TEAM</span>
      <img src="assets/img/logo/tekscaleup-logo.svg" alt="TekScaleUp"><div class="ts-services-brand-disciplines"><span>Technology</span><span>Design</span><span>AI</span></div>
    </section>'''))
    brand = cls('ts-services-brand',main)[0]
    brand.getparent().replace(brand,deepcopy(cls('tp-banner-area',doc)[0]))
    listing = deepcopy(services)
    stage = cls('tp-service-pin',listing)[0]
    template = deepcopy(cls('tp-service-item',listing)[0])
    for node in list(stage):
        stage.remove(node)
    data = [('startup-scaleup', 'Startup & Scaleup Services', 'Build and improve your digital product with web and mobile app development, supported by design and code audits.', ['Web Development', 'Mobile App Development', 'Design Audit', 'Code Audit'], 'startup-20261013.png', 'Startup & Scaleup Services'), ('ai-connected-technology', 'AI & Connected Technology', 'Develop intelligent applications, chatbots and AI agents. Automate workflows and connect devices through IoT.', ['AI & ML Development', 'Chatbots & AI Agents', 'AI Automation', 'IoT'], 'ai-20261013.png', 'AI & Connected Technology'), ('cloud-it-services', 'Cloud & IT Services', 'Build the infrastructure behind your applications with DevOps, cloud infrastructure, cybersecurity, systems and networking.', ['DevOps', 'Cloud Infrastructure', 'Cybersecurity', 'Systems & Networking'], 'cloud-20261013.png', 'Cloud & IT Services'), ('design-branding', 'Design & Branding', 'Shape clear digital experiences and a consistent brand through UI/UX design, web and mobile app design, prototyping and brand identity.', ['UI/UX Design', 'Web/Mobile App Design', 'Prototyping', 'Brand Identity'], 'design-20261013.png', 'Design & Branding')]
    for i,(slug,title,description,tags,image,selection) in enumerate(data,1):
        panel = deepcopy(template)
        panel.set('id',slug)
        text(cls('tp-service-number',panel)[0].xpath('./span')[0],f'{i:02}.')
        heading = panel.xpath('.//h4')[0]
        heading.tag = 'h2'
        text(heading.xpath('./a')[0],title)
        text(cls('tp-service-content',panel)[0].xpath('./p')[0],description)
        target='software-development.html' if slug=='startup-scaleup' else slug+'.html'
        text(cls('tp-btn-black-text',panel)[0],'Explore this service')
        for a in panel.xpath('.//a'):
            a.set('href',target)
            a.attrib.pop('data-enquiry-service',None)
        content(cls('tp-service-category',panel)[0],''.join('<a href="'+target+'#capability-'+str(n)+'">'+tag+'</a>' for n,tag in enumerate(tags,1)))
        img = cls('tp-service-thumb',panel)[0].xpath('./img')[0]
        img.set('src','assets/img/services/'+image)
        img.set('alt',title+' illustration in TekScaleUp blue and green')
        # Each reused SVG button filter needs its own ID.
        for node in panel.xpath('.//*[@id]'):
            old = node.get('id')
            new = f'service-button-{i}'
            node.set('id',new)
            for target in panel.iter():
                for attr,value in list(target.attrib.items()):
                    if attr != 'id':
                        target.set(attr,value.replace(old,new))
        stage.append(panel)
    main.append(listing)
    main.append(deepcopy(projects))
    main.append(deepcopy(work))
    # Shared contact and footer already sit outside main in the original template.
    for a in page.xpath('//a[@href]'):
        href = a.get('href')
        if href.startswith('#') and href not in ('#top','#contact','#services','#projects','#process'):
            a.set('href','index.html'+href)
    for a in page.xpath('//a[@href="#top"]'):
        a.set('href','index.html')
    text(page.xpath('//title')[0],'Services & Capabilities | TekScaleUp')
    for node in page.xpath('//link[@rel="canonical"]'):
        node.set('href','https://tekscaleup.com/services.html')
    for node in page.xpath('//meta[@property="og:url"]'):
        node.set('content','https://tekscaleup.com/services.html')
    for node in page.xpath('//meta[@name="description"] | //meta[@property="og:description"]'):
        node.set('content','Explore TekScaleUp services: startup and scaleup services, cloud and IT services, AI and connected technology, design and branding.')
    page.xpath('//head')[0].append(etree.Element('link',rel='stylesheet',href='assets/css/services.css?v=20261013'))
    page.xpath('//body')[0].append(etree.Element('script',src='assets/js/services.js?v=20261013'))
    (ROOT/'services.html').write_text('<!doctype html>\n'+html.tostring(page,encoding='unicode',method='html'),encoding='utf-8')
