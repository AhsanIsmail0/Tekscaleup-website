"""Build a local, dependency-free SVG from Natural Earth public-domain geography."""
from pathlib import Path
from math import radians, pi
import json
from html import escape

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/'tmp/map-source/countries.geojson').read_text(encoding='utf-8'))

def project(lon, lat):
    lam, phi = radians(lon), radians(lat)
    p2, p4 = phi*phi, phi**4
    x = lam*(.8707-.131979*p2+p4*(-.013791+p4*(.003971*p2-.001529*p4)))
    y = phi*(1.007226+p2*(.015085+p4*(-.044475+.028874*p2-.005916*p4)))
    return 500+169*x, 263-169*y

def line(coords, close=False):
    return 'M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in (project(*c[:2]) for c in coords))+('Z' if close else '')

def geometry(g):
    polygons = [g['coordinates']] if g['type']=='Polygon' else g['coordinates']
    return ''.join(line(ring,True) for polygon in polygons for ring in polygon)

parts=['<svg xmlns="http://www.w3.org/2000/svg" class="ts-world-map" viewBox="0 0 1000 510" width="1000" height="510" role="group" aria-labelledby="ts-map-title ts-map-description"><title id="ts-map-title">TekScaleUp global presence</title><desc id="ts-map-description">Select Pakistan, Canada or Japan to see our locations. Other countries are shown for geographic context.</desc>']
parts.append('<g class="ts-map-grid" aria-hidden="true">')
for lat in range(-60,86,15):
    parts.append(f'<path d="{line([(lon,lat) for lon in range(-180,181,3)])}"/>')
for lon in range(-180,181,20):
    parts.append(f'<path d="{line([(lon,lat) for lat in range(-60,86,3)])}"/>')
parts.append('</g><g class="ts-map-land" aria-hidden="true">')
offices={}
for f in data['features']:
    name=f['properties']['ADMIN']
    if name=='Antarctica': continue
    d=geometry(f['geometry'])
    if name in ('Canada','Pakistan','Japan'): offices[name]=d
    else: parts.append(f'<path d="{d}"/>')
parts.append('</g>')
anchors={'Canada':(-114.0719,51.0447),'Pakistan':(74.3587,31.5204),'Japan':(140.1233,35.6073)}
parts.append('<g class="ts-map-connections" aria-hidden="true">')
for start,end,lift in [('Pakistan','Canada',110),('Pakistan','Japan',40)]:
    x1,y1=project(*anchors[start]);x2,y2=project(*anchors[end])
    parts.append(f'<path data-route="{end.lower()}" d="M{x1:.2f},{y1:.2f} C{x1+(x2-x1)*.3:.2f},{min(y1,y2)-lift:.2f} {x1+(x2-x1)*.7:.2f},{min(y1,y2)-lift:.2f} {x2:.2f},{y2:.2f}"/>')
parts.append('</g>')
for name in ('Canada','Pakistan','Japan'):
    slug=name.lower();x,y=project(*anchors[name]);selected=name=='Pakistan'
    parts.append(f'<g class="ts-map-country{" is-active" if selected else ""}" data-location="{slug}" role="button" tabindex="0" aria-label="Show TekScaleUp locations in {name}" aria-controls="ts-map-detail" aria-pressed="{str(selected).lower()}"><path class="ts-map-office-land" d="{offices[name]}"/>')
    parts.append(f'<circle class="ts-map-hit" cx="{x:.2f}" cy="{y:.2f}" r="24"/><circle class="ts-map-halo" cx="{x:.2f}" cy="{y:.2f}" r="13"/><circle class="ts-map-pin" cx="{x:.2f}" cy="{y:.2f}" r="5"/>')
    dx,dy,align=(18,-18,'start') if name=='Canada' else ((-16,32,'end') if name=='Pakistan' else (16,30,'start'))
    parts.append(f'<text class="ts-map-label" x="{x+dx:.2f}" y="{y+dy:.2f}" text-anchor="{align}" aria-hidden="true">{name}</text></g>')
parts.append('</svg>')
svg=''.join(parts)
(ROOT/'assets/img/brand/global-presence-map.svg').write_text(svg,encoding='utf-8')
markup=f'''<section id="global-presence" class="ts-global-presence" aria-labelledby="ts-presence-heading">
<div class="container container-1300">
<div class="ts-map-heading"><div><span class="tp-section-subtitle pre">Our global presence</span><h2 id="ts-presence-heading">Three countries.<br><span>One team.</span></h2></div><p>Pakistan, Canada and Japan.<br>Select a location to connect.</p></div>
<div class="ts-map-canvas">{svg}</div>
<div class="ts-map-locations" role="group" aria-label="Choose a country">
<button type="button" class="ts-location-button is-active" data-location="pakistan" aria-controls="ts-map-detail" aria-pressed="true"><span class="ts-location-index">01</span><span><strong>Pakistan</strong><span>Lahore</span></span><span class="ts-location-arrow" aria-hidden="true">↗</span></button>
<button type="button" class="ts-location-button" data-location="canada" aria-controls="ts-map-detail" aria-pressed="false"><span class="ts-location-index">02</span><span><strong>Canada</strong><span>Calgary &amp; Edmonton</span></span><span class="ts-location-arrow" aria-hidden="true">↗</span></button>
<button type="button" class="ts-location-button" data-location="japan" aria-controls="ts-map-detail" aria-pressed="false"><span class="ts-location-index">03</span><span><strong>Japan</strong><span>Yotsukaido, Chiba</span></span><span class="ts-location-arrow" aria-hidden="true">↗</span></button>
</div>
<div id="ts-map-detail" class="ts-map-detail" role="status" aria-live="polite" aria-atomic="true"><span class="ts-location-dot" aria-hidden="true"></span><strong data-map-country>Pakistan</strong><span data-map-cities>Z-tower, Q-block, Johar Town, Lahore, Pakistan</span><a href="#contact" aria-label="Contact the TekScaleUp team">Connect with our team <span aria-hidden="true">↗</span></a></div>
</div></section>'''
(ROOT/'tmp/global-map-section.html').write_text(markup,encoding='utf-8')
(ROOT/'tmp/map-source/README.md').write_text('Geography: Natural Earth 1:110m admin 0 countries, public domain.\nhttps://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_admin_0_countries.geojson\nProjection: Natural Earth 1, following the official D3 implementation (ISC license).\nhttps://github.com/d3/d3-geo/blob/main/src/projection/naturalEarth1.js\nCity pins indicate geographic locations; the map does not represent service coverage.\n',encoding='utf-8')
print('Generated world map with 3 interactive countries and locally stored geography.')
