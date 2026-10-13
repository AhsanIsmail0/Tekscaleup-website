from copy import deepcopy
from html import escape
from lxml import html, etree

def build(ROOT):
    source=html.parse(str(ROOT/'software-development.html')).getroot()
    data=[('software-development','Startup & Scaleup Services','Software built<br>around <span>you.</span>','Web and mobile applications, design audits and code audits for your next stage of growth.','startup-20261013.png',[('Web Development','Build web experiences around your users and business requirements.'),('Mobile App Development','Develop mobile applications around the tasks your users need to complete.'),('Design Audit','Review usability, user journeys and interface consistency.'),('Code Audit','Assess code quality and identify technical improvements.')]),('ai-connected-technology','AI & Connected Technology','Intelligence with<br>a <span>purpose.</span>','Turn a specific business challenge into an AI application, an automated workflow or a connected device experience.','ai-20261013.png',[('AI & ML Development','Develop models and applications around your data, requirements and evaluation criteria.'),('Chatbots & AI Agents','Build conversational tools and agents with clearly defined tasks and boundaries.'),('AI Automation','Connect intelligent tools with repeatable business workflows and human review.'),('IoT','Connect devices and applications to collect and use operational data.')]),('cloud-it-services','Cloud & IT Services','A stronger<br><span>foundation.</span>','Connect infrastructure, delivery workflows and security requirements with the systems your business relies on.','cloud-20261013.png',[('DevOps','Improve application delivery through deployment workflows and automation.'),('Cloud Infrastructure','Plan and configure cloud environments around application requirements.'),('Cybersecurity','Assess security requirements and implement safeguards within an agreed scope.'),('Systems & Networking','Connect and configure the systems and networks behind your operations.')]),('design-branding','Design & Branding','Clear experiences.<br>Distinct <span>identity.</span>','Bring your product experience and visual identity together through purposeful design and prototyping.','design-20261013.png',[('UI/UX Design','Shape user journeys and interfaces around the people using your product.'),('Web/Mobile App Design','Design responsive web and mobile app experiences with consistent visual patterns.'),('Prototyping','Explore interaction concepts before moving into development.'),('Brand Identity','Create a coherent visual identity that reflects your business.')])]
    portfolio=[('Geepas UAE','geepas','https://uae.geepas.com/','Electronics and appliances website'),('Wigme','wigme','https://wigme.com/','Multi-brand retail website'),('FAMS','fams','https://fams.com/','Connected operations platform')]
    for n,(slug,title,heading,description,image,capabilities) in enumerate(data,1):
        page=deepcopy(source);body=page.xpath('//body')[0];body.set('data-service',title)
        def one(cls):return page.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," '+cls+' ")]')[0]
        def settext(node,value):
            for c in list(node):node.remove(c)
            node.text=value
        hero=one('ts-detail-heading');settext(hero.xpath('./span')[0],f'{n:02} / {title}')
        h=hero.xpath('./h1')[0];h.clear();h.set('class','tp-char-animation');h.append(html.fromstring('<span class="ts-detail-title-lines">'+heading+'</span>'))
        settext(one('ts-detail-intro').xpath('./p')[0],description)
        settext(one('ts-detail-visual-copy').xpath('./span')[0],title)
        settext(one('ts-detail-visual-copy').xpath('./p')[0],'Built around your next challenge.')
        img=one('ts-detail-visual-frame').xpath('./img')[0];img.set('src','assets/img/services/'+image);img.set('alt',title+' illustration')
        tags=one('ts-detail-visual-tags');tags.clear();tags.set('class','ts-detail-visual-tags')
        for label,_ in capabilities:tags.append(html.fromstring('<span>'+escape(label)+'</span>'))
        for article,(label,copy) in zip(one('ts-detail-capability-list').xpath('./article'),capabilities):
            settext(article.xpath('./h3')[0],label);settext(article.xpath('./div/p')[0],copy)
            ul=article.xpath('./div/ul')[0];ul.getparent().remove(ul)
        settext(one('ts-detail-section-head').xpath('./h2')[0],'Built for your next step.')
        # Scope-neutral questions also apply to infrastructure, AI and design projects.
        questions=[('Can you work with our existing setup?','We begin by reviewing your current setup, requirements and constraints before agreeing the scope.'),('What do you need to estimate a project?','Share your goals, current challenge, available materials and any timeline or budget constraints.'),('How long will the work take?','The timeline depends on scope, complexity, dependencies and review cycles. We agree a delivery plan after discovery.'),('How are scope changes handled?','We discuss the impact on deliverables, timing and cost before agreeing changes.'),('What about handover and ongoing support?','Handover, ownership and support arrangements are agreed as part of the project scope and contract.')]
        for item,(q,a) in zip(one('ts-detail-faq-list').xpath('./details'),questions):settext(item.xpath('./summary')[0],q);settext(item.xpath('./p')[0],a)
        main=page.xpath('//main')[0]
        # Client supplied portfolio links establish references, not a verified delivery scope.
        related=html.fromstring('<section class="ts-related-projects" id="related-projects"><div class="container container-1750"><span class="tp-section-subtitle">Portfolio references</span><h2>Related <span>projects.</span></h2><p class="ts-related-note">Explore selected portfolio references. Service-specific delivery scope and results are not yet documented.</p><div class="ts-related-grid"></div><div data-projects-button></div></div></section>')
        cards=related.xpath('.//*[@class="ts-related-grid"]')[0]
        selected=[portfolio[2]] if slug=='ai-connected-technology' else portfolio[:2]
        if slug=='cloud-it-services':selected=[]
        for name,asset,url,context in selected:
            cards.append(html.fromstring('<article><a href="'+url+'" target="_blank" rel="noopener noreferrer"><img loading="lazy" src="assets/img/portfolio/'+asset+'.webp" alt="'+name+' website preview"><h3>'+name+' <span>↗</span></h3></a><p>'+context+'</p><small>Contribution scope awaiting confirmation.</small></article>'))
        if not selected:
            cards.append(html.fromstring('<p class="ts-case-note">Cloud and IT case studies will be added once the delivery scope is confirmed. Explore our wider project portfolio below.</p>'))
        button=deepcopy(one('tp-header-btn-box').xpath('./a')[0]);button.set('href','projects.html')
        for el in button.xpath('.//*[@id]'):
            old=el.get('id');el.set('id','related-projects-button')
            for target in button.iter():
                for attr,value in list(target.attrib.items()):
                    if attr!='id':target.set(attr,value.replace(old,'related-projects-button'))
        settext(button.xpath('.//*[contains(@class,"tp-btn-black-text")]')[0],'Explore All Projects')
        related.xpath('.//*[@data-projects-button]')[0].append(button)
        main.insert(4,related)
        links=html.fromstring('<section class="ts-other-services"><div class="container container-1750"><h2>Explore other services.</h2><div></div><a href="services.html">All Services ↗</a></div></section>')
        for other,label,*_ in data:
            if other!=slug:links.xpath('.//div/div')[0].append(html.fromstring('<a href="'+other+'.html">'+escape(label)+' ↗</a>'))
        main.append(links)
        settext(page.xpath('//title')[0],title+' | TekScaleUp')
        for meta in page.xpath('//meta[@name="description"] | //meta[@property="og:description"]'):meta.set('content',description)
        for meta in page.xpath('//meta[@property="og:title"]'):meta.set('content',title+' | TekScaleUp')
        for meta in page.xpath('//meta[@property="og:url"]'):meta.set('content','https://tekscaleup.com/'+slug+'.html')
        canonical=page.xpath('//link[@rel="canonical"]')
        if canonical: canonical[0].set('href','https://tekscaleup.com/'+slug+'.html')
        else: page.xpath('//head')[0].append(etree.Element('link',rel='canonical',href='https://tekscaleup.com/'+slug+'.html'))
        settext(page.xpath('//*[@id="ts-enquiry-title"]')[0],'Tell us about your project.')
        settext(one('ts-detail-intro').xpath('.//*[contains(@class,"tp-btn-black-text")]')[0],'Discuss your project')
        (ROOT/(slug+'.html')).write_text('<!doctype html>\n'+html.tostring(page,encoding='unicode'),encoding='utf-8')
