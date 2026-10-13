"""End-to-end checks against the loopback CMS preview; removes only records created by this test."""
import urllib.request,urllib.error,http.cookiejar,json,uuid,sqlite3
from pathlib import Path
BASE='http://127.0.0.1:8774';jar=http.cookiejar.CookieJar();client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar));created=[]
def req(path,method='GET',data=None,expected=200,auth=True):
 headers={'X-CMS-Request':'1','Origin':BASE};body=None
 if data is not None:body=json.dumps(data).encode();headers['Content-Type']='application/json'
 r=urllib.request.Request(BASE+'/api/'+path,data=body,headers=headers,method=method)
 try:
  response=(client if auth else urllib.request.build_opener()).open(r);status=response.status;result=json.load(response)
 except urllib.error.HTTPError as e:status=e.code;result=json.load(e)
 assert status==expected,(path,status,result);return result
try:
 req('admin/content',expected=401,auth=False);req('session','POST',{},auth=True)
 for kind in ['services','projects','blogs','jobs']:
  slug='qa-'+uuid.uuid4().hex
  data=dict(type=kind,title='QA draft '+kind,slug=slug,summary='End-to-end test content.',body='First paragraph.\n\nSecond paragraph.',image='',url='',tags=['First capability'],category='QA',status='draft',sortOrder=9999,location='Remote',employmentType='Contract')
  record=req('admin/content','POST',data,201)['item'];created.append(record['id'])
  assert not any(i['id']==record['id'] for i in req('content')['items'])
  data.update(version=1,status='published');record=req('admin/content/'+record['id'],'PUT',data)['item']
  assert any(i['id']==record['id'] for i in req('content')['items'])
  req('admin/content/'+record['id'],'PUT',data,409)
  data.update(version=2,status='archived');record=req('admin/content/'+record['id'],'PUT',data)['item']
  assert not any(i['id']==record['id'] for i in req('content')['items'])
  data.update(version=3,status='draft');req('admin/content/'+record['id'],'PUT',data)
 raw=(Path(__file__).resolve().parents[1]/'assets/img/services/design-20261013.png').read_bytes()
 upload=urllib.request.Request(BASE+'/api/media',data=raw,headers={'X-CMS-Request':'1','Origin':BASE,'Content-Type':'image/png'},method='POST')
 with client.open(upload) as response: media=json.load(response)
 assert media['url'].startswith('/assets/img/uploads/')
 with client.open(BASE+media['url']) as response: assert response.status==200 and response.read(8)==b'\x89PNG\r\n\x1a\n'
 uploaded=(Path(__file__).resolve().parents[1]/media['url'].lstrip('/')).resolve()
 assert uploaded.parent==Path(__file__).resolve().parents[1]/'assets/img/uploads'
 uploaded.unlink()
 bad=dict(type='blogs',title='Unsafe',slug='unsafe',summary='Bad URL',status='draft',image='javascript:alert(1)')
 req('admin/content','POST',bad,400)
 req('admin/content','POST',dict(type='jobs',slug='missing',status='draft'),400)
 print('PASS: auth boundary, all four content types, persistence, draft isolation, publish, archive/restore, stale edit conflict and unsafe URL rejection.')
finally:
 with sqlite3.connect(Path(__file__).resolve().parents[1]/'backups/cms-local.sqlite3') as c:
  for ident in created:c.execute('DELETE FROM content WHERE id=?',(ident,))
