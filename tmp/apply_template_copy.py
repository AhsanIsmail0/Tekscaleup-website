from pathlib import Path
from copy import deepcopy
from lxml import html, etree
from html import escape

ROOT = Path(__file__).resolve().parents[1]
doc = html.fromstring((ROOT / 'tmp/index_4.before-content.html').read_text(encoding='utf-8'))

# User requested removal of the stock image/video gallery.
for gallery in doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," tp-video-area ")]'):
    gallery.getparent().remove(gallery)

def cls(name, parent=doc):
    return parent.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " ' + name + ' ")]')

def content(node, markup):
    for child in list(node):
        node.remove(child)
    node.text = None
    for piece in html.fragments_fromstring(markup):
        if isinstance(piece, str):
            if len(node):
                node[-1].tail = (node[-1].tail or '') + piece
            else:
                node.text = (node.text or '') + piece
        else:
            node.append(piece)

def text(node, value):
    content(node, escape(value))

def section(name, ident):
    node = cls(name)[0]
    node.set('id', ident)
    return node

def external(node, url):
    node.set('href', url)
    node.set('target', '_blank')
    node.set('rel', 'noopener noreferrer')

doc.set('lang', 'en')
doc.xpath('//body')[0].set('id', 'top')
text(doc.xpath('//title')[0], 'TekScaleUp - Technology & Marketing Solutions')
doc.xpath('//meta[@name="description"]')[0].set('content', 'TekScaleUp delivers software, UI/UX design, digital marketing, cloud infrastructure, cybersecurity and emerging technology solutions. Connect with our global team.')
nav = cls('tp-mobile-menu-active')[0]
content(nav, '<ul>' + ''.join(f'<li><a href="#{anchor}">{label}</a></li>' for anchor, label in [('about','About'),('services','Services'),('projects','Projects'),('people','The People'),('contact','Contact')]) + '</ul>')
for a in doc.xpath('//a[contains(@class,"tp-btn-black")]'):
    a.set('href', '#contact')
for node in cls('tp-offcanvas-title'):
    if 'Hello' in node.text_content():
        text(node, 'Let’s work together.')
text(cls('tp-offcanvas-content')[0].xpath('.//p')[0], 'Technology, marketing and the right people for your next project.')
content(cls('tp-offcanvas-contact')[0].xpath('.//ul')[0], '<li><a href="mailto:contact@tekscaleup.com">contact@tekscaleup.com</a></li><li>Pakistan · Canada · Japan</li>')
content(cls('tp-offcanvas-social')[0].xpath('.//ul')[0], '<li><a href="https://www.linkedin.com/company/23724699/" target="_blank" rel="noopener noreferrer" aria-label="TekScaleUp on LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a></li><li><a href="https://www.instagram.com/tekscaleup/" target="_blank" rel="noopener noreferrer" aria-label="TekScaleUp on Instagram"><i class="fa-brands fa-instagram"></i></a></li>')
cls('tp-offcanvas-social')[0].xpath('.//ul')[0].append(html.fromstring('<li><a href="https://www.facebook.com/tekscaleup/" target="_blank" rel="noopener noreferrer" aria-label="TekScaleUp on Facebook"><i class="fa-brands fa-facebook-f"></i></a></li>'))
cls('tp-offcanvas-open-btn')[0].set('aria-label', 'Open menu')
cls('tp-offcanvas-close-btn')[0].set('aria-label', 'Close menu')

# Connect the original animated typography to one real project preview.
hero = cls('tp-hero-title')[0]
hero.tag = 'h1'
hero_area = cls('tp-hero-area')[0]
hero_area.set('class', hero_area.get('class') + ' ts-hero')
hero_row = hero.getparent().getparent().getparent()
hero_row.set('class', 'row align-items-center ts-hero-row')
left, right = list(hero_row)
left.set('class', 'col-xl-7')
right.set('class', 'col-xl-5')
content(hero, '<span class="ts-hero-line">Your technology team.</span><span class="ts-hero-line">Your marketing team.</span><span class="ts-hero-line ts-hero-partner">One partner.</span>')
hero.set('aria-label', 'Your technology team. Your marketing team. One partner.')
left.append(html.fromstring('<div class="ts-hero-summary tp_text_anim"><p>We build software, run infrastructure, and help businesses reach their customers.</p></div>'))
button = deepcopy(cls('tp-btn-black')[0])
for node in button.iter():
    for attr, value in list(node.attrib.items()):
        if 'buttonFilter' in value:
            node.set(attr, value.replace('buttonFilter', 'heroButtonFilter'))
text(cls('tp-btn-black-text', button)[0], 'Discuss your project')
button.set('href', '#contact')
actions = html.fromstring('<div class="ts-hero-actions tp_fade_anim" data-delay="1.2"></div>')
actions.append(button)
left.append(actions)
content(right, '<div class="ts-hero-proof tp_fade_anim" data-delay="2.2" data-fade-from="right"><div class="ts-hero-proof-label"><span>Featured project</span><span>Geepas UAE</span></div><a class="ts-hero-project" href="https://uae.geepas.com/" target="_blank" rel="noopener noreferrer" aria-label="Explore the Geepas UAE project in a new tab"><div class="ts-browser-bar" aria-hidden="true"><i></i><i></i><i></i><span>uae.geepas.com</span></div><img src="assets/img/portfolio/geepas.webp" alt="Geepas UAE homepage" width="1260" height="710" fetchpriority="high"><div class="ts-hero-project-caption"><div><strong>Geepas UAE</strong><span>Electronics &amp; appliances</span></div><svg width="22" height="22" viewBox="0 0 22 22" fill="none" aria-hidden="true"><path d="M1 21L21 1M21 1H1M21 1V21" stroke="currentColor" stroke-width="1.5"/></svg></div></a></div>')

about = section('tp-about-area', 'about')
about_image = cls('tp-about-thumb')[0].xpath('./img')[0]
about_image.set('src', 'assets/img/brand/about-brand.svg')
about_image.set('alt', 'White TekScaleUp icon on brand blue')
for node in cls('tp-about-shape-1') + cls('tp-about-avater-info')[0].xpath('./img'):
    node.getparent().remove(node)
banner_image = cls('tp-banner-img')[0].xpath('./img')[0]
banner_image.set('src', 'assets/img/brand/project-green.svg')
banner_image.set('alt', '')
banner_image.set('aria-hidden', 'true')
logo_wallpaper = etree.Element('div', {'class': 'ts-project-logo-wallpaper', 'data-speed': '.7', 'role': 'img', 'aria-label': 'Scattered project logos: Geepas, Wigme, Electromart, Grasscity, Smoke Cartel, Daily High Club, FAMS and DankStop'})
banner_image.getparent().append(logo_wallpaper)
text(cls('tp-about-text')[0].xpath('./p')[0], 'TekScaleUp brings technology, design and marketing together to solve business challenges. We build digital products, strengthen IT operations and help businesses reach their customers.')
content(cls('tp-about-avater-info')[0].xpath('.//p')[0], 'A global network of technical expertise,<br> with a presence in Pakistan, Canada and Japan.')
for counter, label, value in zip(cls('tp-about-funcact-item'), ['Clients<br>worldwide', 'Completed<br>projects'], ['20', '100']):
    digit = counter.xpath('.//i')[0]
    digit.set('data-purecounter-end', value)
    digit.tail = '+'
    content(counter.xpath('./p')[0], label)

for node, label in zip(cls('tp-text-slide-title'), ['Software Development','UI/UX Design','Digital Marketing','Cloud & Security','AI & IoT','Technology Partner'] * 5):
    text(node, label)

services = section('tp-service-area', 'services')
service_data = [
    ('Software & Design', 'Build the tools your business needs, from websites and e-commerce platforms to custom software and ERP systems. Our UI/UX team makes complex experiences clear and practical.', ['Web & E-commerce','Custom Software','UI/UX Design','ERP Solutions']),
    ('Cloud & Security', 'Support your daily operations with managed cloud infrastructure, network monitoring and cybersecurity. Our NOC and SOC services help your team maintain the systems it relies on.', ['Cloud Infrastructure','NOC & SOC','Cybersecurity','IT Operations']),
    ('Digital Marketing', 'Plan your digital presence around the customers you want to reach. We combine digital strategy, social media management and creative content to support your marketing campaigns.', ['Digital Strategy','Social Media','Creative Content','Business Growth']),
    ('AI & Emerging Tech', 'Develop AI and machine learning applications, connect devices through IoT, and explore Web3. We also create 3D animation and immersive AR, VR and MR experiences, with technical training to support your team.', ['AI & Machine Learning','IoT & Web3','AR / VR / MR','3D & Training']),
]
for panel, (title, description, tags) in zip(cls('tp-service-item'), service_data):
    text(panel.xpath('.//h4/a')[0], title)
    panel.xpath('.//h4/a')[0].set('href', '#contact')
    text(cls('tp-service-content', panel)[0].xpath('./p')[0], description)
    text(cls('tp-btn-black-text', panel)[0], 'Discuss your project')
    content(cls('tp-service-category', panel)[0], ''.join(f'<span>{escape(tag)}</span>' for tag in tags))

for panel, slug, alt in zip(cls('tp-service-item'), ['software-design','cloud-security','digital-marketing','ai-emerging-tech'], ['Software interface design and component development','Protected cloud infrastructure and connected servers','Campaign planning across search, social media and email','Operational data flowing through an AI model into actionable insights']):
    service_image = cls('tp-service-thumb', panel)[0].xpath('./img')[0]
    service_image.set('src', f'assets/img/services/{slug}-v3.webp')
    service_image.set('alt', alt)

projects = section('tp-project-area', 'projects')
project_data = [
    ('Geepas UAE','https://uae.geepas.com/','geepas','Electronics & appliances'),
    ('Wigme','https://wigme.com/','wigme','Multi-brand retail'),
    ('Electromart','https://electromart.com.gh/','electromart','Electronics & home appliances'),
    ('Grasscity','https://www.grasscity.com/','grasscity','Specialty retail'),
    ('Smoke Cartel','https://www.smokecartel.com/','smoke-cartel','Specialty retail'),
    ('Daily High Club','https://dailyhighclub.com/','daily-high-club','Subscriptions & retail'),
    ('FAMS','https://fams.com/','fams','Enterprise AI & connected operations'),
    ('DankStop','https://dankstop.com/','dankstop','Specialty retail'),
]
columns = cls('tp-project-item')[0].getparent().getparent()
column_nodes = list(columns)
template = deepcopy(cls('tp-project-item')[0])
for column in column_nodes:
    for item in list(column):
        column.remove(item)
for index, (name, url, slug, category) in enumerate(project_data):
    item = deepcopy(template)
    for a in item.xpath('.//a'):
        external(a, url)
    thumb = cls('tp-project-thumb', item)[0]
    thumb.set('data-cursor', 'View<br>Project')
    a = thumb.xpath('./a')[0]
    a.set('data-displacement', 'assets/img/home-01/webgl/1.webp')
    a.set('aria-label', f'Open {name} project in a new tab')
    image = a.xpath('./img')[0]
    image.set('src', f'assets/img/portfolio/{slug}.webp' if slug != 'grasscity' else 'assets/img/portfolio/grasscity-brand.webp')
    image.set('alt', f'{name} homepage preview' if slug != 'grasscity' else 'Grasscity brand logo on TekScaleUp green')
    bar = html.fromstring(f'<div class="ts-browser-bar" aria-hidden="true"><i></i><i></i><i></i><span>{url.split("//")[1].rstrip("/")}</span></div>')
    thumb.insert(0, bar)
    text(cls('tp-project-title', item)[0].xpath('./a')[0], name)
    content(cls('tp-project-category', item)[0], f'<span>{escape(category)}</span>')
    column_nodes[index % 2].append(item)
text(cls('tp-project-link')[0].xpath('.//*[contains(@class,"tp-btn-black-text")]')[0], 'Start your project')

# Keep the original three pinned metric panels and animated digit spans.
facts = cls('tp-funfact-panel')
for panel, title, number in zip(facts, ['Global tech<br>resources', 'Clients<br>worldwide', 'Partner<br>companies'], ['100','20+','200']):
    content(cls('tp-funfact-title', panel)[0], title)
    for node, digit in zip(cls('tp-funfact-number', panel)[0].xpath('.//*[contains(@class,"tp-text-bounce")]'), number):
        text(node, digit)
    for subtitle in cls('tp-funfact-subtitle', panel):
        text(subtitle, '( Our network )')
content(cls('tp-funfact-number', facts[2])[0], '<span><span class="tp-text-bounce" data-delay="1">2</span><span class="tp-text-bounce" data-delay="1.3">0</span><i class="tp-text-bounce" data-delay="1.6">0</i></span>')

work = section('tp-work-area', 'process')
content(cls('tp-work-title-box')[0].xpath('.//h2')[0], 'From<br> idea to<br> delivery')
for item, title, description in zip(cls('tp-work-item'), ['Understand your goals','Plan the solution','Design & build','Test & launch'], [
    'We start with your business, your users and the challenge you need to solve. Together, we define the priorities.',
    'We agree on the scope, approach and delivery plan, bringing the right skills together for your project.',
    'We turn the plan into working designs and technology, sharing progress and incorporating your feedback.',
    'We test the experience, prepare for launch and help you identify the next improvements.'
]):
    text(cls('tp-work-title', item)[0], title)
    text(cls('tp-work-content', item)[0].xpath('./p')[0], description)

section('tp-testimonial-area', 'recommendations')
text(cls('tp-testimonial-title-box')[0].xpath('.//h4')[0], 'Professional Recommendations')
rating = cls('tp-testimonial-ratting')[0]
content(rating, '<div class="tp-testimonial-ratting-info"><p>About our people · From the company profile</p></div>')
quotes = [
    ('Chris Orsini','Director IT, KellerWilliams','I have worked with Arsam on multiple projects and have been very impressed with his project management and the products he and his team have developed.'),
    ('Prof. Hellen Bontempo','Founder & Business Owner, Abound English School','Arsam is one of the most dedicated professionals with his work. Working with Arsam, I found him as a person with great knowledge and deep background in modern business solutions.'),
    ('Alan Tao','Digital Marketing Agency Director, Amazing Web Services','Arsam Is Very Helpful and Cares About his work. He shown me his dedication and the commitment to do a good work. I am impressed by his follow up, attention and ability to fulfill the job on time.'),
    ('Carl A. Young','Data, IT, and Cyber Professional','His intellect is razor-sharp and his patience and desire to help others is always present.'),
    ('Muhammad Faisal Arshad','Finance Operations & Transformation','Arsam javed is a pleasure to work with, and has outstanding experience in business development, project management, stakeholder management.'),
    ('Haider Aly-Reza','Fintech Business Development & Operations','Arsam’s client management and project management skills have laid a key foundation for the success of the company.'),
]
for item, (name, role, quote) in zip(cls('tp-testimonial-item'), quotes):
    text(cls('tp-testimonial-text', item)[0].xpath('./p')[0], '“' + quote + '”')
    info = cls('tp-testimonial-author-info', item)[0]
    text(info.xpath('./span')[0], name)
    text(info.xpath('./p')[0], role)
    avatar = cls('tp-testimonial-avater', item)[0]
    content(avatar, f'<span class="ts-quote-initials" aria-hidden="true">{escape("".join(n[0] for n in name.split()[:2]))}</span>')

# Reuse the award list's existing reveal animation and row design for the people.
people = section('tp-award-area', 'people')
text(cls('tp-award-subtitle')[0], '( The People )')
for box, city, country in zip(cls('tp-award-img'), ['Lahore','Calgary & Edmonton','Chiba'], ['Pakistan','Canada','Japan']):
    content(box, f'<span class="tp-section-subtitle">{country}</span><h4>{city}</h4>')
# Replace the existing location labels with the interactive global-presence map.
city_row = cls('tp-award-img')[0].getparent().getparent()
city_row.getparent().remove(city_row)
people.addprevious(html.fromstring((ROOT/'tmp/global-map-section.html').read_text(encoding='utf-8')))
leaders = [('President','Syed Muhammad Ayub Shah','https://www.linkedin.com/in/sayub/','AS'),('CEO','Arsam Javed','https://www.linkedin.com/in/arsam-javed/','AJ'),('CTO','Usman Munier','https://www.linkedin.com/in/usmanmunier/','UM'),('CFO','Zafar Ullah','https://www.linkedin.com/in/zafar-ullah-ab051365/','ZU')]
leader_dir = ROOT / 'assets/img/people'
leader_dir.mkdir(exist_ok=True)
for row, (role, name, url, initials) in zip(cls('tp-award-item'), leaders):
    row.tag = 'a'
    row.set('class', row.get('class') + ' d-block')
    external(row, url)
    row.set('aria-label', f'{name}, {role}, on LinkedIn')
    text(cls('tp-award-year', row)[0], role)
    text(cls('tp-award-text', row)[0], name)
    text(cls('tp-award-position', row)[0], 'LinkedIn')
    image_path = f'assets/img/people/{initials.lower()}-portrait-v1.webp'
    row.set('data-person', initials.lower())
    person_box = cls('tp-award-box-left', row)[0]
    person_info = etree.Element('div', {'class': 'ts-person-info'})
    for child in list(person_box):
        person_info.append(child)
    person_box.append(etree.Element('img', {'class': 'ts-person-thumb', 'src': image_path, 'alt': '', 'width': '88', 'height': '104', 'loading': 'lazy'}))
    person_box.append(person_info)
    reveal = cls('tp-award-reveal-img', row)[0]
    reveal.set('data-background', image_path)
    reveal.set('role', 'img')
    reveal.set('aria-label', f'Portrait of {name}')
for row in cls('tp-award-item')[4:]:
    row.getparent().remove(row)

footer = section('tp-footer-area', 'contact')
content(cls('tp-footer-widget-title')[0], 'Your technology<br> &amp; marketing partner.')
content(cls('tp-footer-widget-menu')[0].xpath('./ul')[0], ''.join(f'<li><a href="#{anchor}">{label}</a></li>' for anchor,label in [('about','About'),('services','Services'),('projects','Projects'),('process','Our Process'),('global-presence','Our Locations'),('people','The People'),('contact','Contact')]))
info = cls('tp-footer-widget-info')
content(info[0], '<a href="mailto:contact@tekscaleup.com">contact@tekscaleup.com</a>')
content(info[1], '<p>104-A, Avenue 3, NFC Phase 1<br>Lahore, Pakistan</p><p>Pakistan · Canada · Japan</p>')
social = cls('tp-footer-widget-social')[0]
content(social, ''.join(f'<a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="TekScaleUp on {name}"><span><i class="fa-brands fa-{icon}"></i></span></a>' for name,icon,url in [('LinkedIn','linkedin-in','https://www.linkedin.com/company/23724699/'),('Facebook','facebook-f','https://www.facebook.com/tekscaleup/'),('Instagram','instagram','https://www.instagram.com/tekscaleup/')]))
content(cls('tp-copyright-right')[0], '<a href="#contact">Contact</a><a href="https://www.linkedin.com/company/23724699/" target="_blank" rel="noopener noreferrer">LinkedIn</a>')

# The baseline references missing decorative files. Keep existing components,
# using available assets rather than leaving broken images or unavailable scripts.
for image in doc.xpath('//img[@src]'):
    source = image.get('src')
    if source.startswith('assets/') and not (ROOT/source).is_file():
        replacement = {'assets/img/offcanvas/offcanvas-4.webp':'assets/img/offcanvas/offcanvas-4.jpg'}.get(source)
        if replacement:
            image.set('src', replacement)
        elif 'testimonial/global' in source or 'testimonial/overlay' in source:
            image.getparent().remove(image)
        else:
            image.set('src', 'assets/img/logo/tekscaleup-icon.svg')
            image.set('alt', '')
for node in doc.xpath('//*[@data-background]'):
    source = node.get('data-background')
    if source.startswith('assets/') and not (ROOT/source).is_file():
        del node.attrib['data-background']
for script in doc.xpath('//script[@src]'):
    source = script.get('src')
    if source.startswith('assets/') and not (ROOT/source).is_file():
        script.getparent().remove(script)
    if '/libs/isotope/' in source:
        script.set('src', source.replace('/libs/isotope/', '/libs/jquery.isotope/'))
for a in doc.xpath('//a[@href]'):
    href = a.get('href')
    if href == 'assets/img/offcanvas/offcanvas-4.webp':
        a.set('href', 'assets/img/offcanvas/offcanvas-4.jpg')
    elif href in ('index_4.html', 'index.html'):
        a.set('href', '#top')
    elif href.endswith('.html'):
        a.set('href', '#contact')

head = doc.xpath('//head')[0]
# Remove the unrelated stock-image gallery from the original menu.
for gallery in cls('tp-offcanvas-gallery'):
    gallery.getparent().remove(gallery)
for stylesheet in head.xpath('.//link[@href="assets/css/main.css"]'):
    stylesheet.set('href', 'assets/css/main.min.css')
head.append(etree.Element('link', rel='preload', href='assets/fonts/inter-latin-variable.woff2', **{'as': 'font', 'type': 'font/woff2', 'crossorigin': 'anonymous'}))
description = doc.xpath('//meta[@name="description"]')[0].get('content')
for key, value in [('og:type','website'), ('og:title','TekScaleUp | Your technology & marketing partner'), ('og:description',description), ('og:image','https://tekscaleup.com/assets/img/brand/social-share.png'), ('og:image:width','1200'), ('og:image:height','630'), ('og:image:alt','TekScaleUp. Technology, design and marketing. Pakistan, Canada and Japan.')]:
    head.append(etree.Element('meta', property=key, content=value))
head.append(etree.Element('meta', name='twitter:card', content='summary_large_image'))
head.append(etree.Element('meta', name='twitter:image', content='https://tekscaleup.com/assets/img/brand/social-share.png'))
head.append(etree.Element('link', rel='stylesheet', href='assets/css/template-content.css'))
doc.xpath('//body')[0].append(etree.Element('script', src='assets/js/template-content.js'))
doc.xpath('//body')[0].append(etree.Element('script', src='assets/js/global-map.js'))
for node in doc.xpath('//script[@src] | //link[@rel="stylesheet"]'):
    attr = 'src' if node.tag == 'script' else 'href'
    value = node.get(attr, '')
    if value.startswith('assets/'):
        node.set(attr, value.split('?')[0] + '?v=map-motion-20261010-3')
result = '<!doctype html>\n' + html.tostring(doc, encoding='unicode', method='html')
for path in ('index.html','index_4.html'):
    (ROOT / path).write_text(result, encoding='utf-8')
print('Applied TekScaleUp content to original template. Original animation classes and button markup retained.')
