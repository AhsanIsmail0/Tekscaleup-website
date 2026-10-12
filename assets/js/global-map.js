/* Local orthographic globe. Scroll moves the camera; office cards appear on arrival. */
(() => {
  const section = document.querySelector('.ts-cinematic-presence');
  if (!section) return;
  const offices = [
    {key:'pakistan', country:'Pakistan', city:'Lahore', lon:74.3587, lat:31.5204, pins:[[74.3587,31.5204,'Lahore']]},
    {key:'canada', country:'Canada', city:'Calgary & Edmonton', lon:-114.0719, lat:52.25, pins:[[-114.0719,51.0447,'Calgary'],[-113.4938,53.5461,'Edmonton']]},
    {key:'japan', country:'Japan', city:'Yotsukaido, Chiba', lon:140.168, lat:35.669, pins:[[140.168,35.669,'Yotsukaido']]}
  ];
  const svg = section.querySelector('.ts-cinematic-globe');
  const buttons = [...section.querySelectorAll('.ts-location-button')];
  const cards = [...section.querySelectorAll('[data-office]')];
  const caption = section.querySelector('[data-globe-caption]');
  const status = section.querySelector('.ts-globe-status');
  const camera = {lon:38, lat:20, zoom:.94, active:0, card:1};
  let render = () => {}, motion, scrollTimeline, manual = false, lastIndex = -1;
  let stacked = false, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const syncCards = () => {
    const index = Math.max(0,Math.min(2,Math.round(camera.active)));
    cards.forEach((card,i) => {
      const visible = stacked || (i === index && camera.card > .01);
      card.classList.toggle('is-current',i === index);
      card.setAttribute('aria-hidden',String(!visible));
      card.inert = !visible;
      if (!stacked) {
        card.style.opacity = i === index ? camera.card : 0;
        card.style.transform = `translateY(${(1-camera.card)*20}px)`;
      } else { card.style.removeProperty('opacity'); card.style.removeProperty('transform'); }
    });
    if (index !== lastIndex) {
      buttons.forEach((button,i) => {button.classList.toggle('is-active',i === index);button.setAttribute('aria-pressed',String(i === index));});
      caption.textContent = `${offices[index].country} / ${offices[index].city}`;
      lastIndex = index;
    }
  };
  const update = () => {syncCards();render();};
  const nearestLongitude = target => camera.lon + ((target-camera.lon+540)%360)-180;
  const choose = index => {
    manual = true;
    motion?.kill();
    const destination = offices[index];
    if (!window.gsap || reduce) {Object.assign(camera,{lon:destination.lon,lat:destination.lat,zoom:1.2,active:index,card:1});update();}
    else {
      motion = gsap.timeline({onUpdate:update});
      motion.to(camera,{card:0,zoom:.9,duration:.3,ease:'power2.inOut'})
        .to(camera,{lon:nearestLongitude(destination.lon),lat:destination.lat,duration:1.05,ease:'power2.inOut'})
        .set(camera,{active:index})
        .to(camera,{zoom:1.27,card:1,duration:.65,ease:'power3.out'});
    }
    status.textContent = `${destination.country}: ${destination.city}. Office address and company registration details shown.`;
  };
  buttons.forEach((button,index) => {
    button.addEventListener('click',()=>choose(index));
    button.addEventListener('keydown',event=>{
      const offset = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0;
      if (!offset) return;
      event.preventDefault();
      const next = (index+offset+3)%3;
      buttons[next].focus({preventScroll:true});choose(next);
    });
  });
  const resume = () => {if (!manual) return;manual=false;motion?.kill();scrollTimeline?.invalidate();};
  window.addEventListener('wheel',resume,{passive:true});
  window.addEventListener('touchmove',resume,{passive:true});
  window.addEventListener('keydown',event=>{if(['PageDown','PageUp','ArrowDown','ArrowUp','Home','End'].includes(event.key))resume();});
  syncCards();
  const init = async () => {
    if (!window.d3?.geoOrthographic) return;
    const response = await fetch(new URL('../img/brand/globe-countries.json', document.currentScript?.src || new URL('assets/js/global-map.js', document.baseURI)));
    if (!response.ok) throw new Error('Geography unavailable');
    const geography = await response.json();
    geography.features.forEach(feature => {
      if (d3.geoArea(feature) > 2*Math.PI) {
        const polygons = feature.geometry.type === 'Polygon' ? [feature.geometry.coordinates] : feature.geometry.coordinates;
        polygons.forEach(polygon=>polygon.forEach(ring=>ring.reverse()));
      }
    });
    const ns = 'http://www.w3.org/2000/svg';
    const createPath = parent => {const path=document.createElementNS(ns,'path');parent.append(path);return path;};
    const sphere = createPath(svg.querySelector('[data-globe-sphere]'));
    const grid = createPath(svg.querySelector('[data-globe-grid]'));
    const land = geography.features.map(feature=>({feature,path:createPath(svg.querySelector('[data-globe-land]'))}));
    const pins = offices.flatMap((office,index)=>office.pins.map(([lon,lat,label],pinIndex)=>{
      const g=document.createElementNS(ns,'g');
      g.setAttribute('class','ts-globe-pin');
      const ring=document.createElementNS(ns,'circle');ring.setAttribute('r','10');ring.setAttribute('class','ts-globe-pin-ring');g.append(ring);
      const dot=document.createElementNS(ns,'circle');dot.setAttribute('r','3.5');dot.setAttribute('class','ts-globe-pin-dot');g.append(dot);
      const text=document.createElementNS(ns,'text');text.textContent=label;text.setAttribute('x','16');text.setAttribute('y',String(pinIndex ? -13 : 22));g.append(text);
      svg.querySelector('[data-globe-pins]').append(g);return {g,index,lon,lat};
    }));
    const projection=d3.geoOrthographic().translate([400,310]).clipAngle(90).precision(.5);
    const path=d3.geoPath(projection), graticule=d3.geoGraticule10();
    render = () => {
      projection.rotate([-camera.lon,-camera.lat,0]).scale(258*camera.zoom);
      sphere.setAttribute('d',path({type:'Sphere'}));grid.setAttribute('d',path(graticule));
      const index=Math.round(camera.active);
      land.forEach(({feature,path:element})=>{element.setAttribute('d',path(feature)||'');element.classList.toggle('is-office',offices.some(o=>o.country===feature.properties.name));element.classList.toggle('is-selected',offices[index].country===feature.properties.name);});
      pins.forEach(({g,index:pinIndex,lon,lat})=>{
        const visible=d3.geoDistance([lon,lat],[camera.lon,camera.lat])<Math.PI/2-.035;
        g.style.display=visible ? '' : 'none';
        if (!visible) return;
        const point=projection([lon,lat]);g.setAttribute('transform',`translate(${point[0]},${point[1]})`);
        g.classList.toggle('is-selected',pinIndex===index);
        g.querySelector('text').style.opacity=pinIndex===index && camera.zoom>1.05 ? '1' : '0';
      });
    };
    section.classList.add('globe-ready');update();
    if (!window.gsap || !window.ScrollTrigger) return;
    gsap.matchMedia().add({desktop:'(min-width: 992px) and (min-height: 760px)',small:'(max-width: 991px), (max-height: 759px)',reduce:'(prefers-reduced-motion: reduce)'},context=>{
      reduce=context.conditions.reduce;stacked=context.conditions.small || reduce;
      section.classList.toggle('is-stacked-globe',stacked);
      if (stacked) {camera.card=1;update();return()=>{section.classList.remove('is-stacked-globe');stacked=false;};}
      section.classList.add('has-globe-story');
      const story={lon:38,lat:20,zoom:.9,active:0,card:0};
      scrollTimeline=gsap.timeline({onUpdate:()=>{if(!manual){Object.assign(camera,story);update();}},scrollTrigger:{id:'tekscaleup-globe-story',trigger:section,start:'top 80px',end:()=>'+='+Math.round(innerHeight*2.8),pin:true,scrub:.7,anticipatePin:1,invalidateOnRefresh:true}});
      scrollTimeline.to(story,{lon:74.3587,lat:31.5204,zoom:1.27,duration:.85,ease:'power2.inOut'})
        .to(story,{card:1,duration:.3}).to(story,{duration:.65})
        .to(story,{card:0,zoom:.88,duration:.4,ease:'power2.inOut'})
        .to(story,{lon:245.9281,lat:52.25,duration:1.2,ease:'power2.inOut'})
        .set(story,{active:1}).to(story,{zoom:1.27,card:1,duration:.55,ease:'power2.out'}).to(story,{duration:.65})
        .to(story,{card:0,zoom:.88,duration:.4})
        .to(story,{lon:140.168,lat:35.669,duration:1.05,ease:'power2.inOut'})
        .set(story,{active:2}).to(story,{zoom:1.27,card:1,duration:.55,ease:'power2.out'}).to(story,{duration:.65})
        .to(story,{zoom:.92,lat:25,duration:.6,ease:'power2.inOut'});
      return()=>{section.classList.remove('has-globe-story');motion?.kill();manual=false;camera.card=1;update();};
    });
    document.fonts?.ready.then(()=>ScrollTrigger.refresh());
  };
  init().catch(()=>{section.classList.add('globe-unavailable');camera.card=1;syncCards();});
})();
