import {identity,validate,imageExtension} from '../lib/cms.js';
import {login,logout} from '../lib/password-auth.js';
const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
const item=row=>({...JSON.parse(row.payload),id:row.id,version:row.version,updatedAt:row.updated_at});
export async function onRequest({request,env}){
 const url=new URL(request.url),path=url.pathname.replace(/^\/api\/?/,'');
 try{
  if(path==='session'&&request.method==='POST'&&!env.ACCESS_TEAM_DOMAIN&&!env.ACCESS_AUD)return await login(request,env);
  if(path==='session'&&request.method==='DELETE')return logout(request);
  if(path.startsWith('media/')&&request.method==='GET'){if(!env.MEDIA)return json({error:'Media storage unavailable.'},503);const key=path.slice(6);if(!/^[a-f0-9-]+\.(png|jpg|webp)$/.test(key))return json({error:'Not found'},404);const object=await env.MEDIA.get(key);if(!object)return json({error:'Not found'},404);return new Response(object.body,{headers:{'Content-Type':object.httpMetadata?.contentType||'application/octet-stream','X-Content-Type-Options':'nosniff','Cache-Control':'public,max-age=86400'}});}
  if(path==='content'&&request.method==='GET'){if(!env.DB)return json({error:'Content database unavailable.'},503);const rows=await env.DB.prepare("SELECT * FROM content WHERE status='published'").all();const all=await env.DB.prepare('SELECT payload,status FROM content').all();const routes=all.results.map(r=>({page:JSON.parse(r.payload).page,published:r.status==='published'})).filter(r=>r.page);return json({items:rows.results.map(item).sort((a,b)=>a.sortOrder-b.sortOrder),routes});}
  const email=await identity(request,env);
  if(path==='session'&&request.method==='GET')return json({authenticated:true,email,local:false,uploads:!!env.MEDIA});
  if(request.method!=='GET'&&(request.headers.get('X-CMS-Request')!=='1'||request.headers.get('Origin')!==url.origin))return json({error:'Invalid request origin.'},403);
  if(path==='media'&&request.method==='POST'){if(!env.MEDIA)return json({error:'Media storage unavailable.'},503);if(Number(request.headers.get('Content-Length'))>5242880)return json({error:'Maximum image size is 5 MB.'},413);const bytes=new Uint8Array(await request.arrayBuffer());if(bytes.length>5242880)return json({error:'Maximum image size is 5 MB.'},413);const mime=request.headers.get('Content-Type'),ext=imageExtension(bytes,mime),key=crypto.randomUUID()+'.'+ext;await env.MEDIA.put(key,bytes,{httpMetadata:{contentType:mime}});return json({url:'/api/media/'+key},201);}
  if(!env.DB)return json({error:'Content database unavailable.'},503);
  if(path==='admin/content'&&request.method==='GET'){const rows=await env.DB.prepare('SELECT * FROM content ORDER BY updated_at DESC').all();return json({items:rows.results.map(item)});}
  if((path==='admin/content'&&request.method==='POST')||(path.startsWith('admin/content/')&&request.method==='PUT')){
   if(Number(request.headers.get('Content-Length'))>65000)return json({error:'Content is too large.'},413);
   const raw=await request.text();if(new TextEncoder().encode(raw).length>65000)return json({error:'Content is too large.'},413);const input=JSON.parse(raw),data=validate(input),id=request.method==='POST'?crypto.randomUUID():path.split('/').pop(),now=new Date().toISOString();let version=1;
   if(request.method==='PUT'){const old=await env.DB.prepare('SELECT * FROM content WHERE id=?').bind(id).first();if(!old)return json({error:'Content not found.'},404);if(old.type!==data.type)return json({error:'Content type cannot change.'},400);if(old.version!==Number(input.version))return json({error:'Changed in another session. Reload before editing.'},409);const prior=JSON.parse(old.payload);if(prior.page)data.page=prior.page;version=old.version+1;const result=await env.DB.prepare('UPDATE content SET slug=?,payload=?,status=?,version=?,updated_at=? WHERE id=? AND version=?').bind(data.slug,JSON.stringify(data),data.status,version,now,id,old.version).run();if(!result.meta.changes)return json({error:'Concurrent update. Reload and retry.'},409);}
   else await env.DB.prepare('INSERT INTO content(id,type,slug,payload,status,version,updated_at) VALUES(?,?,?,?,?,?,?)').bind(id,data.type,data.slug,JSON.stringify(data),data.status,version,now).run();
   return json({item:{...data,id,version,updatedAt:now}},request.method==='POST'?201:200);
  }
  return json({error:'Not found.'},404);
 }catch(error){const message=String(error.message);if(/UNIQUE constraint/i.test(message))return json({error:'That slug is already used.'},409);const auth=/identity|access|sign in|account|signature|configured|signing key/i.test(message);return json({error:auth?message:'Could not save content. '+(/too long|required|Invalid|secure HTTPS|Sub-service|image/i.test(message)?message:'Please try again.')},auth?403:400);}
}
