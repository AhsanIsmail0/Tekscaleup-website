# Content admin portal

## Working local preview

Run `python tmp/cms_preview.py 8774` from the project folder, then open `http://127.0.0.1:8774/admin/`.
Click **Open local preview**. This development-only entry exists exclusively in the loopback Python server. The production Pages Function has no local-login bypass.

The local database is `backups/cms-local.sqlite3`. Uploaded local images are saved under `assets/img/uploads/`. Restarting the preview keeps content. Back up both before moving machines.

Services, Projects, Blogs and Job openings support create, edit, draft, publish, archive and restore. A version check prevents one edit from silently overwriting another. Slugs are unique within each type. Uploaded images are restricted to PNG, JPEG and WebP up to 5 MB. Content is plain text rendered with DOM textContent, not executable HTML.

Published items feed the public pages through `/api/content`. New services, articles and jobs use `content.html?type=...&slug=...` for their detail page. Existing pages retain their current URLs. Published job applications open the configured application URL or mailto link. No applications are collected or emailed by this portal.

## Production on Cloudflare Free

Use the existing Cloudflare Pages Free project and D1 Free database. Do not activate R2, Zero Trust billing, or Workers Paid for this setup. Free limits apply; account plan upgrades require a separate decision.

1. Bind the D1 database `tekscaleup-content` as `DB`. Initialize content once with `admin/seed.sql`, and run `admin/auth-schema.sql` for login attempt protection. Do not continually re-import the seed.
2. In Pages > Settings > Variables and secrets > Production, the owner must add an encrypted **Secret** named `ADMIN_ACCESS_KEY`. Use a password manager to generate at least 32 random characters. This is the admin login credential. Never commit it, paste it in chat, or place it in a plaintext variable. Rotating the secret invalidates old sessions on the next deployment.
3. Leave `ACCESS_TEAM_DOMAIN` and `ACCESS_AUD` unset for access-key authentication. The optional Access JWT implementation remains available for a future explicitly configured setup.
4. Run `python tmp/build_dashboard.py`. It packages runtime assets, compiles `functions/` into `dist/_worker.js`, and creates `output/tekscaleup-cloudflare.zip`. Upload this ZIP to the Pages production deployment. A static ZIP without `_worker.js` cannot run the backend, but a compiled Worker ZIP is supported by dashboard Direct Upload.
5. Visit `/admin/`, sign in with the access key, and verify drafts, publish/archive, and public updates. No R2 binding is required. Production uses image URL fields or existing `/assets/img/` paths; direct uploads are hidden without a `MEDIA` binding.

Access-key authentication uses an eight-hour, origin-bound, HMAC-signed Secure/HttpOnly/SameSite=Strict host-only cookie, same-origin checks on writes, and D1-backed atomic rate limits of five login attempts per IP and 100 total attempts per 15-minute window. All admin APIs fail closed if the secret is missing or too short. This is one shared administrator credential; the displayed owner email is a label, not email verification. Use a random key and keep it private. Anyone with the key has admin access. Signing out clears the browser cookie; rotating the secret revokes all sessions.

Public content GET routes remain unauthenticated. Optional R2 and Cloudflare Access routes are unused in this free setup. For local development, the loopback-only preview still uses its separate development login.

## Operational limits

- Static HTML remains a fallback when the public API is unavailable. An existing static article can therefore be visible during an API outage even after it was archived in the CMS. For strict withdrawal guarantees, use server-rendered content or remove the static page in the next deployment.
- New content depends on client-side rendering; SSR and social preview metadata for new generic pages are a separate improvement.
- Blog demo labels remain until an imported demo is edited. Confirm editorial copy before replacing demo content.
- Uploads are retained when records are archived so restoring works. Storage cleanup is deliberately manual.
- No rich-text editor, roles beyond the allowed admin email, scheduling or application inbox is included.

## Validation

`python tmp/test_cms.py` tests the loopback API. It creates and removes only its own temporary records. `node --test tmp/cms_validation.test.mjs` exercises production validation and fail-closed authentication without a live Cloudflare account.

Official references:
- https://developers.cloudflare.com/pages/functions/bindings/
- https://developers.cloudflare.com/pages/functions/wrangler-configuration/
- https://developers.cloudflare.com/pages/functions/routing/

- https://developers.cloudflare.com/pages/get-started/direct-upload/
- https://developers.cloudflare.com/pages/functions/advanced-mode/
