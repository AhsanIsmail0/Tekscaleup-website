import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validate,identity,imageExtension} from '../functions/lib/cms.js';
import {onRequest} from '../functions/api/[[path]].js';
import {login,logout,keyIdentity,loginStatus} from '../functions/lib/password-auth.js';
const base={type:'blogs',title:'A useful article',slug:'a-useful-article',summary:'A short introduction.',status:'draft',tags:[],sortOrder:0};
test('admin script references existing HTML controls and preserves UTF-8 labels',()=>{
 const html=readFileSync(new URL('../admin/index.html',import.meta.url),'utf8'),script=readFileSync(new URL('../assets/js/admin.js',import.meta.url),'utf8');
 const ids=new Set([...html.matchAll(/id="([\w-]+)"/g)].map(m=>m[1]));
 const selectors=[...script.matchAll(/\$\('#([\w-]+)'\)/g)].map(m=>m[1]);assert.deepEqual(selectors.filter(id=>!ids.has(id)),[]);
 assert.ok(html.includes('View website ↗'));assert.ok(html.includes('id="login-status"'));
});
test('normalizes valid content',()=>assert.equal(validate(base).status,'draft'));
test('rejects executable URLs and invalid slugs',()=>{assert.throws(()=>validate({...base,image:'javascript:alert(1)'}));assert.throws(()=>validate({...base,slug:'../admin'}));});
test('restricts binary image types',()=>{assert.equal(imageExtension(Uint8Array.from([137,80,78,71]),'image/png'),'png');assert.throws(()=>imageExtension(new TextEncoder().encode('<svg/>'),'image/svg+xml'));});
test('production identity fails closed without configuration',async()=>{await assert.rejects(identity(new Request('https://tekscaleup.com/api/admin/content'),{}));});
test('unauthenticated admin route is blocked',async()=>{const response=await onRequest({request:new Request('https://tekscaleup.com/api/admin/content'),env:{}});assert.equal(response.status,403);});
test('missing public database returns unavailable, not demo records',async()=>{const response=await onRequest({request:new Request('https://tekscaleup.com/api/content'),env:{}});assert.equal(response.status,503);});
test('access key login enforces origin, rate limits, signature, expiry and host',async()=>{
 let count=0;
 const env={ADMIN_ACCESS_KEY:'test-only-'+crypto.randomUUID(),DB:{prepare(){return {bind(){return this}}},async batch(){count++;return [{results:[{attempts:count}]},{results:[{attempts:count}]},{}]}}};
 const request=(password,origin='https://tekscaleup.com')=>new Request('https://tekscaleup.com/api/session',{method:'POST',headers:{Origin:origin,'X-CMS-Request':'1'},body:JSON.stringify({password})});
 assert.equal((await login(request(env.ADMIN_ACCESS_KEY,'https://evil.example'),env)).status,403);
 assert.equal((await login(request('wrong'),env)).status,403);
 const response=await login(request(env.ADMIN_ACCESS_KEY),env);
 assert.equal(response.status,200);
 const cookie=response.headers.get('Set-Cookie');assert.match(cookie,/HttpOnly; SameSite=Strict/);assert.match(cookie,/Secure/);
 const session=(value,url='https://tekscaleup.com/api/session')=>new Request(url,{headers:{Cookie:value}});
 assert.equal(await keyIdentity(session(cookie),env),'arsamjaved@gmail.com');
 await assert.rejects(keyIdentity(session(cookie.replace(/=./,'=X')),env));
 await assert.rejects(keyIdentity(session(cookie,'https://tekscaleup.pages.dev/api/session'),env));
 await assert.rejects(keyIdentity(session(cookie),{...env,ADMIN_ACCESS_KEY:'rotated-'+crypto.randomUUID()}));
 const realNow=Date.now;Date.now=()=>realNow()+28801000;try{await assert.rejects(keyIdentity(session(cookie),env));}finally{Date.now=realNow;}
 count=5;assert.equal((await login(request(env.ADMIN_ACCESS_KEY),env)).status,429);
 assert.match(logout(request('')).headers.get('Set-Cookie'),/Max-Age=0/);
 assert.equal(logout(request('','https://evil.example')).status,403);
});
test('clipboard boundary whitespace is ignored but internal spaces and letter case remain significant',async()=>{
 const password='Test-only passphrase '+crypto.randomUUID();
 const env={ADMIN_ACCESS_KEY:' \r\n'+password+'\n ',DB:{prepare(){return {bind(){return this}}},async batch(){return [{results:[{attempts:1}]},{results:[{attempts:1}]},{}]}}};
 const request=value=>new Request('https://tekscaleup.com/api/session',{method:'POST',headers:{Origin:'https://tekscaleup.com','X-CMS-Request':'1'},body:JSON.stringify({password:value})});
 const response=await login(request(' \n'+password+'\t'),env);assert.equal(response.status,200);
 const cookie=response.headers.get('Set-Cookie');assert.equal(await keyIdentity(new Request('https://tekscaleup.com/api/session',{headers:{Cookie:cookie}}),env),'arsamjaved@gmail.com');
 assert.equal((await login(request(password.toLowerCase()),env)).status,403);
 assert.equal((await login(request(password.replace('only passphrase','only  passphrase')),env)).status,403);
 assert.equal(loginStatus({ADMIN_ACCESS_KEY:' '.repeat(40)}).configured,false);
 const status=loginStatus(env);assert.equal(status.configured,true);assert.ok(!JSON.stringify(status).includes(password));
});
test('anonymous login status exposes configuration readiness but admin content remains protected',async()=>{
 const env={ADMIN_ACCESS_KEY:'test-only-'+crypto.randomUUID()};
 const response=await onRequest({request:new Request('https://tekscaleup.com/api/session'),env});assert.equal(response.status,200);const state=await response.json();assert.equal(state.configured,true);assert.equal(state.authenticated,false);
 const denied=await onRequest({request:new Request('https://tekscaleup.com/api/admin/content'),env});assert.equal(denied.status,403);
});
test('validates JWT signature, audience, expiry and allowed email',async()=>{
 const keys=await crypto.subtle.generateKey({name:'RSASSA-PKCS1-v1_5',modulusLength:2048,publicExponent:new Uint8Array([1,0,1]),hash:'SHA-256'},true,['sign','verify']);
 const jwk=await crypto.subtle.exportKey('jwk',keys.publicKey);jwk.kid='test-key';
 const original=globalThis.fetch;globalThis.fetch=async()=>new Response(JSON.stringify({keys:[jwk]}),{headers:{'Content-Type':'application/json'}});
 const encode=data=>Buffer.from(typeof data==='string'?data:JSON.stringify(data)).toString('base64url');
 const env={ACCESS_TEAM_DOMAIN:'test.cloudflareaccess.com',ACCESS_AUD:'test-aud',ADMIN_EMAILS:'arsamjaved@gmail.com'};
 const claims={iss:'https://test.cloudflareaccess.com',aud:['test-aud'],exp:Math.floor(Date.now()/1000)+300,email:'arsamjaved@gmail.com'};
 async function token(payload){const input=encode({alg:'RS256',kid:'test-key'})+'.'+encode(payload),signature=await crypto.subtle.sign('RSASSA-PKCS1-v1_5',keys.privateKey,new TextEncoder().encode(input));return input+'.'+Buffer.from(signature).toString('base64url');}
 const request=jwt=>new Request('https://tekscaleup.com/api/session',{headers:{'Cf-Access-Jwt-Assertion':jwt}});
 try{assert.equal(await identity(request(await token(claims)),env),'arsamjaved@gmail.com');await assert.rejects(identity(request(await token({...claims,email:'other@example.com'})),env));await assert.rejects(identity(request(await token({...claims,exp:1})),env));await assert.rejects(identity(request(await token({...claims,aud:['wrong']})),env));const valid=await token(claims);await assert.rejects(identity(request(valid.slice(0,-8)+'AAAAAAAA'),env));}finally{globalThis.fetch=original;}
});
