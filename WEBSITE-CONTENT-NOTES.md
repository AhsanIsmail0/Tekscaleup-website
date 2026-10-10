# TekScaleUp content in the original Avron template

The current `index.html` and `index_4.html` use the original template preserved in `tmp/index_4.before-content.html`. The separate replacement layout has been superseded. Do not run `tmp/build_website.py` or use `website.css` / `website.js` for this site; those belong to the rejected layout. Edit both current HTML files directly, or regenerate them with `tmp/apply_template_copy.py`.

## Design and interactions

The approved hero update uses the headline "Your technology team. Your marketing team. One partner." with supporting copy about software, infrastructure and reaching customers. The original character reveal is retained. A copy of the original SVG-filter button links to contact, and a substantial, clickable Geepas homepage preview replaces the tiny heading image and green card. The project preview enters after the headline begins. Desktop uses an asymmetric two-column composition; mobile stacks the message, action and project.

The original `main.css`, `spacing.css`, animation classes, GSAP bundle, ScrollSmoother wrappers, pinned service/process/fact panels, character and text animations, media sections, project displacement hover, Swiper sliders, cursor effects and SVG filter buttons are retained. `brand.css` supplies the TekScaleUp palette. `template-content.css` accommodates content and browser preview bars. `template-content.js` connects section links to the existing ScrollSmoother instance and closes the mobile menu.

Demo navigation becomes working section links. Eight supplied projects occupy the same two-column project layout. The award list's existing reveal rows now contain the four leadership profiles; its three top columns identify company locations. The existing testimonial slider contains six attributed excerpts from the company profile, without the unsupported template Clutch score.

## Sources and editorial choices

- Company positioning, capabilities, metrics, locations and recommendations: user-provided `TekScaleup Company Profile 2026.pptx.pdf`, pages 1–3 and 6–12.
- Portfolio URLs and leadership roles: supplied by the user.
- Contact: `contact@tekscaleup.com`, supplied by the user. No phone number invented.
- President's name: verified from public LinkedIn profile/company post. Other names correspond to the supplied profile URLs. No invented biographies or qualifications.
- Headline wording fits the original large character-animation layout. The introductory copy states the technology and marketing offering directly.
- No project scope, results, unsupported awards, ratings or individual portraits are invented.

## Portfolio assets

The About portrait and wide stock team photograph are replaced with two original SVG compositions made from actual project screenshots. `assets/img/brand/technology-work.svg` shows FAMS and the company's country presence; `assets/img/brand/selected-projects.svg` shows seven supplied portfolio sites. Both keep the original image containers and parallax speeds. Regenerate these assets with `tmp/create_work_visuals.py`.

Seven homepage screenshots were captured on October 10, 2026 and represent each site's current appearance. They appear in browser frames inside the original project components, retaining the displacement hover effect.

Grasscity was blocked by browser site safety. Its portfolio card now uses the actual Grasscity logo in charcoal on brand green, with the real project link retained. No simulated homepage is presented. Replace it with an approved supplied screenshot when available. The user authorized the 21+ confirmations for Smoke Cartel, Daily High Club and DankStop.

## Baseline assets

The original local template referenced absent decorative images, fonts and two absent optional parallax scripts. Missing HTML image references use available brand assets; absent testimonial overlays are omitted; unused missing script references are removed. The actual GSAP runtime and animation files remain. Inter is now hosted locally with its open font license. Missing proprietary font declarations and the unused Google font imports are removed. The template font variables resolve to Inter. The page loads a conservatively compacted `main.min.css`; editable source remains in `main.css`.

The original Isotope CDN path is corrected to `jquery.isotope`. Existing local template scripts remain intact.

## Verification

`tmp/verify_template.py` compares required animation hooks, panel counts and button markup against the original backup, and checks project/leadership counts, anchors and local HTML asset references. Browser checks verify initialized pin spacers, ScrollSmoother transforms, project navigation and responsive menu behavior.


## October 10 polish

See `POLISH-RESTORE.md` for the full restore point, undo command, changes and remaining factual content requirements. Portrait images were supplied by the user; this polish changes their display framing only. Default GSAP animations and buttons are retained; OS reduced-motion preference receives a static presentation.
