from pathlib import Path
from lxml import html
import json,uuid
r=Path('.');items=[]
def add(kind,slug,title,summary,image='',url='',body='',tags=None,page=''):
 items.append(dict(id=str(uuid.uuid5(uuid.NAMESPACE_URL,'tekscaleup/'+kind+'/'+slug)),type=kind,slug=slug,title=title,summary=summary,image=image,url=url,body=body,tags=tags or [],category='',location='',employmentType='',status='published',sortOrder=len(items),page=page))
d=html.parse('services.html')
for panel in d.xpath('//*[@id="services"]//div[contains(concat(" ",normalize-space(@class)," ")," tp-service-item ")]'):
 title=panel.xpath('.//h2')[0].text_content();slug=panel.get('id');page=panel.xpath('.//h2/a/@href')[0];summary=panel.xpath('.//*[contains(@class,"tp-service-content")]/p')[0].text_content();tags=panel.xpath('.//*[contains(@class,"tp-service-category")]/a/text()');add('services',slug,title,summary,'/'+panel.xpath('.//*[contains(@class,"tp-service-thumb")]/img/@src')[0],tags=tags,page=page)
d=html.parse('projects.html')
for panel in d.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," tp-project-item ")]'):
 title=panel.xpath('.//*[contains(@class,"tp-project-title")]')[0].text_content();url=panel.xpath('.//*[contains(@class,"tp-project-title")]/a/@href')[0];image=panel.xpath('.//*[contains(@class,"tp-project-thumb")]//img/@src')[0];summary=panel.xpath('.//*[contains(@class,"tp-project-category")]')[0].text_content();add('projects',title.lower().replace(' ','-'),title,summary,'/'+image,url)
for p in r.glob('blog-*.html'):
 d=html.parse(str(p));title=d.xpath('//h1')[0].text_content();summary=d.xpath('//*[contains(@class,"ts-blog-lead")]')[0].text_content();image=d.xpath('//img[contains(@class,"ts-blog-cover")]/@src')[0];body='\n\n'.join(e.text_content() for e in d.xpath('//*[contains(@class,"ts-blog-body")]/section/*'));add('blogs',p.stem[5:],title,summary,'/'+image,body=body,page=p.name)
(r/'admin/seed.json').write_text(json.dumps(items,indent=2,ensure_ascii=False),encoding='utf-8')
sql=(r/'admin/schema.sql').read_text(encoding='utf-8-sig')+'\n'
for item in items:
 values=[item['id'],item['type'],item['slug'],json.dumps(item,ensure_ascii=False),item['status'],'2026-10-13T00:00:00Z'];quote=lambda x:"'"+x.replace("'","''")+"'";sql+='INSERT OR IGNORE INTO content(id,type,slug,payload,status,updated_at) VALUES('+','.join(map(quote,values))+');\n'
(r/'admin/seed.sql').write_text(sql,encoding='utf-8')
print('Seeded',len(items),'existing records')
