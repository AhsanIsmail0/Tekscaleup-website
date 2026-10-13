// Optional single-admin authentication for accounts without Cloudflare Access.
// The credential is a long random access key stored only as a Pages secret.
const encoder = new TextEncoder();
const cookieName = '__Host-tsu_admin';
function configured(env) {
 if (typeof env.ADMIN_ACCESS_KEY !== 'string' || env.ADMIN_ACCESS_KEY.length < 32)
  throw Error('Secure admin access is not configured.');
 return env.ADMIN_ACCESS_KEY;
}
async function key(env) {
 return crypto.subtle.importKey('raw', encoder.encode(configured(env)), {name:'HMAC',hash:'SHA-256'}, false, ['sign','verify']);
}
const encode = bytes => btoa(String.fromCharCode(...new Uint8Array(bytes))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
function decode(value) { return Uint8Array.from(atob(value.replace(/-/g,'+').replace(/_/g,'/')), c=>c.charCodeAt(0)); }
export async function keyIdentity(request, env) {
 const token = (request.headers.get('Cookie') || '').split(';').map(s=>s.trim()).find(s=>s.startsWith(cookieName+'='))?.slice(cookieName.length+1);
 if (!token || token.length > 600) throw Error('Sign in to the admin portal.');
 const parts=token.split('.');
 if(parts.length!==2)throw Error('Invalid identity.');
 const signingKey=await key(env);
 if(!await crypto.subtle.verify('HMAC',signingKey,decode(parts[1]),encoder.encode('session:'+parts[0])))throw Error('Invalid signature.');
 const claims=JSON.parse(new TextDecoder().decode(decode(parts[0])));
 const now=Math.floor(Date.now()/1000);
 if(!Number.isFinite(claims.exp)||claims.exp<=now||claims.exp>now+28800||claims.origin!==new URL(request.url).origin)throw Error('Expired or invalid identity.');
 return env.ADMIN_EMAILS || 'arsamjaved@gmail.com';
}
export async function login(request, env) {
 configured(env);
 const url=new URL(request.url);
 if(url.protocol!=='https:'||request.headers.get('Origin')!==url.origin||request.headers.get('X-CMS-Request')!=='1')return result({error:'Invalid request origin.'},403);
 if(!env.DB)return result({error:'Content database unavailable.'},503);
 const raw=await request.text();
 if(encoder.encode(raw).length>2048)return result({error:'Invalid sign in.'},400);
 const input=JSON.parse(raw),signingKey=await key(env);
 // D1 atomic upserts enforce limits across isolates, including parallel attempts.
 const now=Math.floor(Date.now()/1000),window=Math.floor(now/900);
 const ip=request.headers.get('CF-Connecting-IP') || 'unknown';
 const ipHash=encode(await crypto.subtle.sign('HMAC',signingKey,encoder.encode('rate:'+ip)));
 const attempts=await env.DB.batch([
  env.DB.prepare('INSERT INTO admin_login_limits (bucket,attempts,expires) VALUES (?,1,?) ON CONFLICT(bucket) DO UPDATE SET attempts=attempts+1 RETURNING attempts').bind('ip:'+ipHash+':'+window,now+1800),
  env.DB.prepare('INSERT INTO admin_login_limits (bucket,attempts,expires) VALUES (?,1,?) ON CONFLICT(bucket) DO UPDATE SET attempts=attempts+1 RETURNING attempts').bind('all:'+window,now+1800),
  env.DB.prepare('DELETE FROM admin_login_limits WHERE expires < ?').bind(now)
 ]);
 if(attempts[0].results[0].attempts>5||attempts[1].results[0].attempts>100)return result({error:'Too many sign-in attempts. Try again in 15 minutes.'},429,{'Retry-After':'900'});
 const expected=await crypto.subtle.sign('HMAC',signingKey,encoder.encode('credential:'+configured(env)));
 if(typeof input.password!=='string'||!await crypto.subtle.verify('HMAC',signingKey,expected,encoder.encode('credential:'+input.password)))return result({error:'Invalid sign in.'},403);
 const payload=encode(encoder.encode(JSON.stringify({exp:now+28800,origin:url.origin,nonce:crypto.randomUUID()})));
 const signature=encode(await crypto.subtle.sign('HMAC',signingKey,encoder.encode('session:'+payload)));
 return result({authenticated:true},200,{'Set-Cookie':cookieName+'='+payload+'.'+signature+'; Path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=28800'});
}
export function logout(request){
 const url=new URL(request.url);
 if(request.headers.get('Origin')!==url.origin||request.headers.get('X-CMS-Request')!=='1')return result({error:'Invalid request origin.'},403);
 return result({authenticated:false},200,{'Set-Cookie':cookieName+'=; Path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=0'});
}
function result(data,status,headers={}){return new Response(JSON.stringify(data),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store',...headers}})}
