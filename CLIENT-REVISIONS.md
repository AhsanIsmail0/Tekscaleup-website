# Client revisions, October 12, 2026

The hero now has a small Canadian flag and an animated SVG illustration connecting technology, design and marketing. It replaces the featured Geepas preview. Existing typography animation and button markup are retained.

Who We Are includes four animated counters. The two additions, 100+ Global Tech Resources and 200+ Partner Companies, come from page 1 of the 2026 company profile.

The homepage features Geepas, Wigme and Electromart in a three-column row. Explore more projects opens projects.html, which contains all eight project links. Tablet and mobile grids adapt to two and one columns.

The separate Our Network metric panels are removed. The global map uses neutral charcoal land, the same editorial typography and dividers as the surrounding sections, and brand blue and green highlights. Country interactions and the desktop scroll sequence remain available. Smaller screens use an unpinned reveal, and reduced motion shows the complete map.

## Local restore

Run `./UNDO-CLIENT-REVISIONS.ps1` from the project root to restore the previous site. The archive at backups/before-client-revisions-20261012-144943 contains 204 original files and passed checksum verification. Restoring saves the current version in a recovery archive first. Newly added, unused files remain on disk.

## Validation

The updated template checks cover preserved scroll hooks and buttons, removed network panels, all four counter values, three homepage projects, eight portfolio projects, local assets, valid anchors, unique IDs and absence of em dashes. Browser checks covered counter completion, desktop column alignment, portfolio navigation, all eight external destinations, map selection, mobile stacking and horizontal overflow. No browser errors were reported during desktop checks.

These revisions are saved locally for review.
