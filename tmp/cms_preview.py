"""Loopback-only CMS preview. Production uses Pages Functions, D1, R2 and Access."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit,unquote
from http.cookies import SimpleCookie
import sqlite3,json,uuid,secrets,datetime,re,sys
ROOT=Path(__file__).resolve().parents[1];DB=ROOT/'backups/cms-local.sqlite3';TOKEN=secrets.token_urlsafe(32)
DB.parent.mkdir(exist_ok=True)
def connection():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
with connection() as c:
 c.executescript((ROOT/'admin/schema.sql').read_text(encoding='utf-8-sig'))
 if not c.execute('SELECT COUNT(*) FROM content').fetchone()[0]:c.executescript((ROOT/'admin/seed.sql').read_text(encoding='utf-8-sig'))
def pack(row):return {**json.loads(row['payload']),'id':row['id'],'version':row['version'],'updatedAt':row['updated_at']}
def validate(data):
 if data.get('type') not in ['services','projects','blogs','jobs']:raise ValueError('Invalid content type.')
 out={'type':data['type']}
 for name,limit in dict(title=160,slug=100,summary=600,body=30000,category=100,image=2000,url=2000,location=120,employmentType=40).items():
  out[name]=str(data.get(name,'')).strip()
  if len(out[name])>limit:raise ValueError(name+' is too long.')
 if not out['title'] or not out['summary'] or not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',out['slug']):raise ValueError('Title, description and valid slug are required.')
 if data.get('status') not in ['draft','published','archived']:raise ValueError('Invalid status.')
 out['status']=data['status'];out['sortOrder']=min(9999,max(0,int(data.get('sortOrder',0))))
 out['tags']=[str(s).strip() for s in data.get('tags',[]) if str(s).strip()][:20]
 if any(len(s)>100 for s in out['tags']):raise ValueError('Sub-service is too long.')
 for name in ['url','image']:
  value=out[name]
  if value and not (re.fullmatch(r'https://[^\s]+',value,re.I) or name=='image' and re.fullmatch(r'/(assets/|api/media/)[a-z0-9_./-]+',value,re.I) or name=='url' and out['type']=='jobs' and re.fullmatch(r'mailto:[^\s?]+@[^\s?]+',value)):raise ValueError('Use HTTPS URLs or approved local image paths.')
 return out
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
 def log_message(self,*args):pass
 def json(self,data,status=200,cookie=None):
  b=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(b)))
  if cookie:self.send_header('Set-Cookie',cookie)
  self.end_headers();self.wfile.write(b)
 def authenticated(self):
  try:
   cookies=SimpleCookie(self.headers.get('Cookie',''));return secrets.compare_digest(cookies.get('cms_preview').value if cookies.get('cms_preview') else '',TOKEN)
  except:return False
 def trusted(self):
  origin=self.headers.get('Origin');return self.headers.get('X-CMS-Request')=='1' and (not origin or origin=='http://'+self.headers.get('Host',''))
 def do_GET(self):
  if self.headers.get('Host') not in ['127.0.0.1:'+str(port),'localhost:'+str(port)]:return self.json({'error':'Invalid host.'},403)
  path=urlsplit(self.path).path
  if path=='/api/session':return self.json({'authenticated':self.authenticated(),'local':True,'email':'arsamjaved@gmail.com' if self.authenticated() else None})
  if path in ['/api/content','/api/admin/content']:
   if path.endswith('admin/content') and not self.authenticated():return self.json({'error':'Sign in to local preview.'},401)
   with connection() as c:rows=c.execute('SELECT * FROM content'+(" WHERE status='published'" if path=='/api/content' else '')).fetchall()
   routes=[]
   if path=='/api/content':
    with connection() as c: all_rows=c.execute('SELECT payload,status FROM content').fetchall()
    routes=[{'page':json.loads(r['payload']).get('page'),'published':r['status']=='published'} for r in all_rows if json.loads(r['payload']).get('page')]
   return self.json({'items':sorted([pack(r) for r in rows],key=lambda r:r['sortOrder']),'routes':routes})
  target=(ROOT/unquote(path).lstrip('/')).resolve()
  allowed=target in [ROOT,ROOT/'admin',ROOT/'admin/index.html'] or (target.parent==ROOT and target.suffix=='.html') or (ROOT/'assets') in target.parents
  if not target.is_relative_to(ROOT) or not allowed:return self.send_error(404)
  if target.is_dir() and target not in [ROOT,ROOT/'admin']:return self.send_error(404)
  super().do_GET()
 def do_POST(self):self.mutate()
 def do_PUT(self):self.mutate()
 def mutate(self):
  if self.headers.get('Host') not in ['127.0.0.1:'+str(port),'localhost:'+str(port)]:return self.json({'error':'Invalid host.'},403)
  path=urlsplit(self.path).path
  if not self.trusted():return self.json({'error':'Invalid request origin.'},403)
  if path=='/api/session' and self.command=='POST':return self.json({'authenticated':True},cookie='cms_preview='+TOKEN+'; HttpOnly; SameSite=Strict; Path=/')
  if not self.authenticated():return self.json({'error':'Sign in to local preview.'},401)
  try:
   size=int(self.headers.get('Content-Length','0'));limit=5242880 if path=='/api/media' else 65000
   if size>limit:return self.json({'error':'Request too large.'},413)
   raw=self.rfile.read(size)
   if path=='/api/media':
    mime=self.headers.get('Content-Type');ext=None
    if mime=='image/png' and raw.startswith(b'\x89PNG\r\n\x1a\n'):ext='png'
    if mime=='image/jpeg' and raw.startswith(b'\xff\xd8\xff'):ext='jpg'
    if mime=='image/webp' and raw[:4]==b'RIFF' and raw[8:12]==b'WEBP':ext='webp'
    if not ext:raise ValueError('Invalid image. Upload PNG, JPEG or WebP.')
    folder=ROOT/'assets/img/uploads';folder.mkdir(exist_ok=True);name=str(uuid.uuid4())+'.'+ext;(folder/name).write_bytes(raw);return self.json({'url':'/assets/img/uploads/'+name},201)
   if not (path=='/api/admin/content' and self.command=='POST' or path.startswith('/api/admin/content/') and self.command=='PUT'):return self.json({'error':'Not found.'},404)
   input=json.loads(raw);data=validate(input);ident=str(uuid.uuid4()) if self.command=='POST' else path.split('/')[-1];now=datetime.datetime.now(datetime.timezone.utc).isoformat();version=1
   with connection() as c:
    if self.command=='PUT':
     old=c.execute('SELECT * FROM content WHERE id=?',(ident,)).fetchone()
     if not old:return self.json({'error':'Not found.'},404)
     if old['type']!=data['type']:raise ValueError('Content type cannot change.')
     if old['version']!=input.get('version'):return self.json({'error':'Changed in another session. Reload before editing.'},409)
     prior=json.loads(old['payload']);data['page']=prior.get('page','');version=old['version']+1
     result=c.execute('UPDATE content SET slug=?,payload=?,status=?,version=?,updated_at=? WHERE id=? AND version=?',(data['slug'],json.dumps(data),data['status'],version,now,ident,old['version']))
     if not result.rowcount:return self.json({'error':'Concurrent edit. Reload and retry.'},409)
    else:c.execute('INSERT INTO content(id,type,slug,payload,status,version,updated_at) VALUES(?,?,?,?,?,?,?)',(ident,data['type'],data['slug'],json.dumps(data),data['status'],version,now))
   self.json({'item':{**data,'id':ident,'version':version,'updatedAt':now}},201 if self.command=='POST' else 200)
  except sqlite3.IntegrityError:self.json({'error':'That slug is already used.'},409)
  except (ValueError,TypeError,KeyError) as e:self.json({'error':str(e)},400)
  except Exception:self.json({'error':'Could not save content.'},500)
port=int(sys.argv[1]) if len(sys.argv)>1 else 8774
print(f'CMS preview: http://127.0.0.1:{port}/admin/',flush=True)
ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
