import {keyIdentity} from './password-auth.js';
const types=['services','projects','blogs','jobs'];
export function validate(input){
 if(!types.includes(input.type))throw Error('Invalid content type.');
 const out={type:input.type};
 for(const [name,max] of Object.entries({title:160,slug:100,summary:600,body:30000,category:100,image:2000,url:2000,location:120,employmentType:40})){out[name]=String(input[name]??'').trim();if(out[name].length>max)throw Error(name+' is too long.');}
 if(!out.title||!out.summary||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(out.slug))throw Error('Title, description and a valid slug are required.');
 if(!['draft','published','archived'].includes(input.status))throw Error('Invalid status.');out.status=input.status;
 for(const name of ['url','image']){const value=out[name];if(value&&!(/^https:\/\/[^\s]+$/i.test(value)||name==='image'&&/^\/(assets\/|api\/media\/)[a-z0-9_./-]+$/i.test(value)||name==='url'&&out.type==='jobs'&&/^mailto:[^\s?]+@[^\s?]+$/.test(value)))throw Error('Use a secure HTTPS URL or an approved local image path.');}
 out.tags=Array.isArray(input.tags)?input.tags.map(String).map(s=>s.trim()).filter(Boolean).slice(0,20):[];if(out.tags.some(t=>t.length>100))throw Error('Sub-service is too long.');
 out.sortOrder=Math.min(9999,Math.max(0,Number(input.sortOrder)||0));return out;
}
export function imageExtension(bytes,mime){if(mime==='image/png'&&bytes[0]===137&&bytes[1]===80&&bytes[2]===78&&bytes[3]===71)return 'png';if(mime==='image/jpeg'&&bytes[0]===255&&bytes[1]===216&&bytes[2]===255)return 'jpg';if(mime==='image/webp'&&new TextDecoder().decode(bytes.slice(0,4))==='RIFF'&&new TextDecoder().decode(bytes.slice(8,12))==='WEBP')return 'webp';throw Error('Invalid image. Upload PNG, JPEG or WebP.');}
export async function identity(request,env){
 if(env.ADMIN_ACCESS_KEY&&!env.ACCESS_TEAM_DOMAIN&&!env.ACCESS_AUD)return keyIdentity(request,env);
 if(!env.ACCESS_TEAM_DOMAIN||!env.ACCESS_AUD)throw Error('Secure admin access is not configured.');
 const cookie=request.headers.get('Cookie')||'';const token=request.headers.get('Cf-Access-Jwt-Assertion')||cookie.split(';').map(s=>s.trim()).find(s=>s.startsWith('CF_Authorization='))?.slice('CF_Authorization='.length);if(!token)throw Error('Sign in with Cloudflare Access.');
 const parts=token.split('.');if(parts.length!==3)throw Error('Invalid identity.');
 const decode=s=>Uint8Array.from(atob(s.replace(/-/g,'+').replace(/_/g,'/')),c=>c.charCodeAt(0));
 const header=JSON.parse(new TextDecoder().decode(decode(parts[0]))),claims=JSON.parse(new TextDecoder().decode(decode(parts[1])));
 const issuer='https://'+env.ACCESS_TEAM_DOMAIN;
 if(header.alg!=='RS256'||claims.iss!==issuer||(!Number.isFinite(claims.exp)||claims.exp<Date.now()/1000)||(claims.nbf&&claims.nbf>Date.now()/1000)||!(Array.isArray(claims.aud)?claims.aud:[claims.aud]).includes(env.ACCESS_AUD))throw Error('Expired or invalid identity.');
 const response=await fetch(issuer+'/cdn-cgi/access/certs');if(!response.ok)throw Error('Identity verification unavailable.');const certs=await response.json(),jwk=certs.keys.find(key=>key.kid===header.kid);if(!jwk)throw Error('Unknown signing key.');
 const key=await crypto.subtle.importKey('jwk',jwk,{name:'RSASSA-PKCS1-v1_5',hash:'SHA-256'},false,['verify']);if(!await crypto.subtle.verify('RSASSA-PKCS1-v1_5',key,decode(parts[2]),new TextEncoder().encode(parts[0]+'.'+parts[1])))throw Error('Invalid signature.');
 const allowed=(env.ADMIN_EMAILS||'arsamjaved@gmail.com').toLowerCase().split(',').map(s=>s.trim());if(!allowed.includes(String(claims.email).toLowerCase()))throw Error('This account is not allowed.');return claims.email;
}
