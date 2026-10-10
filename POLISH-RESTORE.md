# Website polish and undo

The complete website before this polish is saved in:

`backups/before-polish-20261010-164644/workspace.zip`

The archive contains 175 original files. SHA256 checksums are in the adjacent `manifest.json`.

To undo all changes from this polish, run this in PowerShell from `D:\Tekscaleup`:

```powershell
.\UNDO-POLISH.ps1
```

Then refresh the website. The restore checks every archived file before writing anything and saves the current files to a separate recovery ZIP before restoring. It leaves unused new assets in place, but restores the original pages, styles, scripts and generator, so those assets will not affect the restored site.

To check the backup without changing files:

```powershell
.\UNDO-POLISH.ps1 -VerifyOnly
```

Changes: hero spacing and preview balance; semantic H1; local Inter font and removal of missing proprietary font references; conservative CSS compaction; clearer service copy; Grasscity brand card; mobile portrait thumbnails and keyboard reveals; menu focus handling; small-text and arrow contrast; reduced-motion presentation; social preview image and metadata.

The eight project URLs, normal GSAP scroll effects, logo wallpaper, service ticker speed and original animated buttons are retained. Additional repeated slides keep loops seamless on wide displays. Portrait pixels and facial structures are unchanged.

Project delivery scope and results are intentionally not claimed until confirmed. The sharing-image URL assumes the production site will use `https://tekscaleup.com`; update both pages through `tmp/apply_template_copy.py` if deployment uses another hostname.

Rebuild the pages with `tmp/apply_template_copy.py`. Rebuild font/CSS/brand assets with `tmp/polish_assets.py` followed by `tmp/render_polish_assets.cjs`. Run `tmp/verify_template.py` for the template integration checks.
