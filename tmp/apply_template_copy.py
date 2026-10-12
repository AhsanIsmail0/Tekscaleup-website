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

# Preserve the original animated typography with a connected brand illustration.
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
left.append(html.fromstring('<div class="ts-hero-summary tp_text_anim"><p>From customer-facing websites to the systems behind them, we bring development, IT operations and marketing into one working relationship.</p></div>'))
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
left.append(html.fromstring('<p class="ts-hero-evidence"><strong>20+</strong> clients worldwide <span></span> <strong>100+</strong> completed projects</p>'))
hero.getparent().insert(0, html.fromstring('<div class="ts-hero-canada"><img src="assets/img/brand/canada-flag.svg" width="32" height="16" alt="Canada flag"><span>Corporation No. 1705776-8</span></div>'))
content(right, (ROOT/'tmp/hero-system.html').read_text(encoding='utf-8'))

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
text(cls('tp-about-text')[0].xpath('./p')[0], 'Your website, operations and marketing need to work together. Our developers, designers, infrastructure specialists and marketers bring those disciplines into one team, from planning through launch and ongoing support.')
content(cls('tp-about-avater-info')[0].xpath('.//p')[0], 'A global network of technical expertise,<br> with a presence in Pakistan, Canada and Japan.')
counter_template = cls('tp-about-funcact-item')[0].getparent()
counter_row = counter_template.getparent()
for _ in range(2):
    counter_row.append(deepcopy(counter_template))
counter_row.set('class', counter_row.get('class', '') + ' ts-about-counters')
for counter, label, value in zip(cls('tp-about-funcact-item'), ['Clients<br>worldwide', 'Completed<br>projects', 'Global tech<br>resources', 'Partner<br>companies'], ['20', '100', '100', '200']):
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
columns.set('class', 'row ts-project-grid')
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
    descriptions = {
        'geepas': 'An online storefront for electronics and home appliances in the UAE.',
        'wigme': 'A multi-brand retail experience bringing everyday products into one catalogue.',
        'electromart': 'Electronics and home appliances for shoppers in Ghana.',
        'grasscity': 'A specialist retail brand with an extensive online product catalogue.',
        'smoke-cartel': 'A specialist e-commerce storefront built around product discovery.',
        'daily-high-club': 'A retail and subscription brand with recurring product collections.',
        'fams': 'Connected operations and AI-assisted workflows for physical businesses.',
        'dankstop': 'A specialist retail catalogue with product-led browsing.'
    }
    overview = html.fromstring('<div class="ts-project-overview"><p>' + escape(descriptions[slug]) + '</p><a class="ts-project-enquiry" href="#contact">Discuss a similar project <span aria-hidden="true">↗</span></a></div>')
    item.append(overview)
    column = etree.SubElement(columns, 'div', {'class': 'col-lg-4 col-md-6'})
    column.append(item)
for column in column_nodes:
    columns.remove(column)
all_project_columns = [deepcopy(column) for column in columns]
for column in list(columns)[3:]:
    columns.remove(column)
text(cls('tp-project-link')[0].xpath('.//*[contains(@class,"tp-btn-black-text")]')[0], 'Explore more projects')

# The client requested removing the separate Our Network section.
for network in cls('tp-funfact-area'):
    network.getparent().remove(network)

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
people.addprevious(html.fromstring((ROOT/'tmp/cinematic-globe-section.html').read_text(encoding='utf-8')))
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

footer = section('tp-footer-area', 'footer')
enquiry = html.fromstring((ROOT/'tmp/enquiry-section.html').read_text(encoding='utf-8'))
footer.getparent().insert(footer.getparent().index(footer), enquiry)
enquiry_button = deepcopy(button)
enquiry_button.set('href', 'mailto:contact@tekscaleup.com?subject=Project%20enquiry')
for node in enquiry_button.iter():
    for attr,value in list(node.attrib.items()):
        if 'heroButtonFilter' in value: node.set(attr,value.replace('heroButtonFilter','enquiryButtonFilter'))
text(cls('tp-btn-black-text',enquiry_button)[0], 'Email your brief')
cls('ts-enquiry-action',enquiry)[0].append(enquiry_button)
content(cls('tp-footer-widget-title')[0], 'Your technology<br> &amp; marketing partner.')
content(cls('tp-footer-widget-menu')[0].xpath('./ul')[0], ''.join(f'<li><a href="#{anchor}">{label}</a></li>' for anchor,label in [('about','About'),('services','Services'),('projects','Projects'),('process','Our Process'),('global-presence','Our Locations'),('people','The People'),('contact','Contact')]))
info = cls('tp-footer-widget-info')
content(info[0], '<a href="mailto:contact@tekscaleup.com">contact@tekscaleup.com</a>')
content(info[1], '<div class="ts-office-addresses"><address><strong>Pakistan</strong>Z-tower, Q-block, Johar Town,<br>Lahore, Pakistan<small class="ts-footer-registration">TEKSCALEUP (PRIVATE) LIMITED<br>Incorporation No. 0255645<br>Tax Registration No. D522955</small></address><address><strong>Canada</strong>287 Taralake Landing Northeast,<br>Calgary, Alberta, Canada<br>Edmonton, Canada<small class="ts-footer-registration">Tekscaleup corp.<br>Corporation No. 1705776-8</small></address><address><strong>Japan</strong>1867-1 Dainichi, Yotsukaido City,<br>Chiba Prefecture, Japan<br><span lang="ja">千葉県四街道市大日1867-1</span><small class="ts-footer-registration"><span lang="ja">株式会社 SCALE TECH</span><br>Corporate No. 6040001140827</small></address></div>')
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
head.append(etree.Element('link', rel='preload', href='assets/fonts/poppins-latin-400.woff2', **{'as': 'font', 'type': 'font/woff2', 'crossorigin': 'anonymous'}))
description = doc.xpath('//meta[@name="description"]')[0].get('content')
for key, value in [('og:type','website'), ('og:title','TekScaleUp | Your technology & marketing partner'), ('og:description',description), ('og:image','https://tekscaleup.com/assets/img/brand/social-share.png'), ('og:image:width','1200'), ('og:image:height','630'), ('og:image:alt','TekScaleUp. Technology, design and marketing. Pakistan, Canada and Japan.')]:
    head.append(etree.Element('meta', property=key, content=value))
head.append(etree.Element('meta', name='twitter:card', content='summary_large_image'))
head.append(etree.Element('meta', name='twitter:image', content='https://tekscaleup.com/assets/img/brand/social-share.png'))
head.append(etree.Element('link', rel='stylesheet', href='assets/css/template-content.css'))
head.append(etree.Element('link', rel='stylesheet', href='assets/css/cinematic-globe.css'))
doc.xpath('//body')[0].append(etree.Element('script', src='assets/js/template-content.js'))
doc.xpath('//body')[0].append(etree.Element('script', src='assets/js/d3-array.min.js'))
doc.xpath('//body')[0].append(etree.Element('script', src='assets/js/d3-geo.min.js'))
doc.xpath('//body')[0].append(etree.Element('script', src='assets/js/global-map.js'))
for node in doc.xpath('//script[@src] | //link[@rel="stylesheet"]'):
    attr = 'src' if node.tag == 'script' else 'href'
    value = node.get(attr, '')
    if value.startswith('assets/'):
        node.set(attr, value.split('?')[0] + '?v=mobile-stacks-20261012-2')
# Set page navigation after the stock-template link cleanup.
cls('tp-project-link')[0].xpath('.//a')[0].set('href', 'projects.html')
result = '<!doctype html>\n' + html.tostring(doc, encoding='unicode', method='html')
for path in ('index.html','index_4.html'):
    (ROOT / path).write_text(result, encoding='utf-8')
print('Applied TekScaleUp content to original template. Original animation classes and button markup retained.')

# Dedicated portfolio page shares the original navigation, footer and motion scripts.
portfolio = deepcopy(doc)
portfolio_main = portfolio.xpath('//main')[0]
for node in list(portfolio_main):
    portfolio_main.remove(node)
portfolio_main.append(html.fromstring('<section class="ts-projects-intro"><div class="container"><span class="tp-section-subtitle">Our work</span><h1>Projects.<br><span>Built for business.</span></h1><p>Explore the businesses in our portfolio. Select a project to visit its website.</p></div></section>'))
portfolio_projects = deepcopy(projects)
portfolio_projects.set('class', 'tp-project-area ts-projects-page')
portfolio_grid = cls('ts-project-grid', portfolio_projects)[0]
for node in list(portfolio_grid):
    portfolio_grid.remove(node)
for column in all_project_columns:
    portfolio_grid.append(deepcopy(column))
text(cls('tp-section-subtitle', portfolio_projects)[0], 'All projects')
portfolio_link = cls('tp-project-link', portfolio_projects)[0]
portfolio_link.xpath('.//a')[0].set('href', '#contact')
text(cls('tp-btn-black-text', portfolio_link)[0], 'Discuss your project')
portfolio_main.append(portfolio_projects)
text(portfolio.xpath('//title')[0], 'Projects | TekScaleUp')
for a in portfolio.xpath('//a[@href]'):
    href = a.get('href')
    if href.startswith('#') and href not in ('#projects', '#contact', '#top'):
        a.set('href', 'index.html' + href)
(ROOT/'projects.html').write_text('<!doctype html>\n' + html.tostring(portfolio, encoding='unicode', method='html'), encoding='utf-8')
print('Created projects.html with all eight projects.')
