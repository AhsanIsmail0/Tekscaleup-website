# TekScaleUp website

Static company website with the original template's GSAP scroll effects, project portfolio, leadership section and interactive global presence map.

## Preview

Run `python tmp/preview_server.py` from the project root. Open the local URL printed by the server. The home page is `index.html`; `index_4.html` is an identical preview entry point.

## Update and verify

Styles are in `assets/css/brand.css` and `assets/css/template-content.css`. The map behavior is in `assets/js/global-map.js`.

The content generator uses `tmp/index_4.before-content.html` as its template. To rebuild both entry points and check template preservation:

```powershell
python tmp/create_global_map.py
python tmp/apply_template_copy.py
python tmp/verify_template.py
```

Runtime libraries include external CDN dependencies. No build step is required. Serve the root directory on a static host.

Local backup archives, restore scripts, original portrait sources and review output are excluded from Git. Existing local backup instructions refer to files retained on the original workstation. Git commits provide version history for the uploaded website.
