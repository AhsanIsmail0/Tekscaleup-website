# Global presence map

The interactive SVG map sits immediately before The People. It replaces the three static location labels with highlighted country outlines, location pins, subtle connecting routes, a country selector and a live location detail row.

Locations: Pakistan (Lahore), Canada (Calgary and Edmonton), Japan (Chiba). These are the existing company-profile locations. The pins are geographic city markers, not individual office buildings.

Interactions: mouse hover, click or tap, Enter/Space on country shapes, and left/right arrow keys between the country selector buttons. The status row announces country changes to assistive technology. Large selector buttons support mobile use; the map respects the existing reduced-motion rules. No runtime map API or external geography requests are needed.

Source: `tmp/create_global_map.py` builds the inline section and standalone SVG from the local Natural Earth geography in `tmp/map-source`. Run it before `tmp/apply_template_copy.py` when rebuilding. Styles are in `assets/css/template-content.css`; behavior is in `assets/js/global-map.js`.

Undo this map addition, keeping the previous polish, by running from `D:\Tekscaleup`:

```powershell
.\UNDO-MAP.ps1
```

Restore point: `backups/before-global-map-20261010-184106`. The 190-file archive was verified before completion. To verify without restoring, use `-VerifyOnly`.

Validation: original template hook/asset/link checks pass. Browser checks covered all three country selections, SVG-shape selection, keyboard navigation, pressed-state updates, country/city text and mobile overflow/touch-target sizing. Desktop and mobile component screenshots use the same section markup and complete website styles. Full-page screenshot capture returned blank frames at the map's deep scroll position, so component captures were used for visual inspection.

## Scroll sequence

Desktop viewports at least 992px wide and 700px tall use a one-screen GSAP pin beneath the header. Pakistan highlights first, its route draws to Canada, then its route draws to Japan. Reached countries stay green. Scrolling backward reverses the sequence. Manual hover, click and keyboard selection remain available; the next scroll stage resumes automatic selection. Scroll changes do not trigger live-region announcements.

Smaller screens use a simple map reveal without pinning. Reduced motion shows the complete map immediately. Breakpoint changes clean up the pin and animation styles through GSAP matchMedia. The original template scripts and motion hooks remain intact.

Undo only this scroll enhancement, keeping the interactive map, with `.\UNDO-MAP-MOTION.ps1`. The restore archive contains 201 files and passed checksum verification.
