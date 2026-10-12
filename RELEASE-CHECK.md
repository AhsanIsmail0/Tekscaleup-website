# Release check

Checked on 12 October 2026, before deployment.

- 82 unused assets removed after saving a full local source archive. Approximately 26.7 MB removed from the active asset tree.
- Local dependency audit: 55 runtime files, no missing dependencies. All 55 returned HTTP 200 from the local preview.
- All local JavaScript files passed Node syntax checks. Git whitespace checks passed.
- Both home entry points match. Three featured projects and eight portfolio projects retained.
- Internal anchor targets, unique IDs, original button markup and GSAP hooks passed the preservation verifier.
- Browser check: no captured JavaScript errors, no broken loaded images, 176 globe country paths, no horizontal overflow on desktop or at 388px mobile width.
- Mobile service and project stacks initialize; desktop has no mobile stack classes. Reduced-motion users receive ordinary document flow.
- Contact draft correctly encodes entered text and targets contact@tekscaleup.com. No email was sent.

Deploy `dist/` or extract `output/tekscaleup-deployment.zip` into the host document root. Regenerate with `python tmp/package_site.py` after edits.

Before launch, confirm the production domain and its DNS. Social preview URLs currently assume tekscaleup.com. Contact sending still relies on the visitor's email application. CDN dependencies still require an internet connection. No live deployment or GitHub push was performed during this cleanup.

Local rollback archive: `backups/before-release-cleanup-20261012-195806.zip`. It contains the full source as it stood immediately before cleanup, including the mobile stacking changes.
