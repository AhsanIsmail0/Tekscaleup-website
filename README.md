# TekScaleUp website

Static company website with the original template's GSAP scroll effects, project portfolio, leadership section and interactive global presence map.

## Preview

Run `python tmp/preview_server.py` from the project root. Open the local URL printed by the server. The home page is `index.html`; `index_4.html` is an identical preview entry point.

## Update and verify

Styles are in `assets/css/brand.css`, `assets/css/template-content.css` and `assets/css/cinematic-globe.css`. The map behavior is in `assets/js/global-map.js`. Mobile service and project scroll stacks live in `assets/js/template-content.js`; desktop GSAP behavior stays in `assets/js/main.js`.

The content generator uses `tmp/index_4.before-content.html` as its template. To rebuild both entry points and check template preservation:

```powershell
python tmp/apply_template_copy.py
python tmp/verify_template.py
```

The cinematic globe uses `tmp/cinematic-globe-section.html`; the older flat-map generator is a fallback source. Runtime libraries include external CDN dependencies. No application build or server is required.

## Prepare deployment

Run `python tmp/package_site.py`. This validates local dependencies and generates `dist/` plus `output/tekscaleup-deployment.zip`. Deploy **only `dist/`**, with `index.html` at the document root. Source scripts, QA pages, originals and backup archives are excluded. On a Git-connected static host, use `dist` as the output directory and run this packaging script during the build (Python with lxml is needed), or upload the generated folder directly.

The contact section opens a mail draft addressed to `contact@tekscaleup.com`; it does not submit to a backend. Social preview metadata currently uses `https://tekscaleup.com`. Confirm the production domain before launch. The project descriptions give business context; no unverified delivery claims or performance results are included.

Poppins font and D3 licences are included in the deployment. Unused legacy template assets were archived locally before removal. Editable `main.css` and project logo sources remain available for maintenance, while the deployment includes only runtime files.

Local backup archives, restore scripts, original portrait sources and review output are excluded from Git. Existing local backup instructions refer to files retained on the original workstation. Git commits provide version history for the uploaded website.
