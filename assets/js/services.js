(() => {
  // Jump links use the scroll timeline rather than the transformed pinned panels.
  const jump = hash => {
    const stage = document.querySelector('#services .tp-service-pin');
    const panels = [...stage.querySelectorAll('.tp-service-item')];
    const index = panels.findIndex(panel => '#'+panel.id === hash);
    if (hash !== '#services' && index < 0) return false;
    const mobile = window.ScrollTrigger?.getAll().find(trigger => trigger.trigger === stage);
    let y;
    if (mobile) y = mobile.start + (index > 0 ? (mobile.end-mobile.start) * index/(panels.length-1) : 0);
    else {
      const target = index < 0 ? document.getElementById('services') : panels[index];
      const trigger = window.ScrollTrigger?.getAll().find(trigger => trigger.trigger === target);
      y = trigger ? trigger.start : target.getBoundingClientRect().top + scrollY - 100;
    }
    const smoother = window.ScrollSmoother?.get();
    if(smoother) smoother.scrollTo(Math.max(0,y),true);
    else if(window.gsap && !matchMedia('(prefers-reduced-motion: reduce)').matches) gsap.to(window,{scrollTo:Math.max(0,y),duration:.7,overwrite:true});
    else window.scrollTo(0,Math.max(0,y));
    document.querySelector('.tp-offcanvas-area')?.classList.remove('opened');
    document.querySelector('.body-overlay')?.classList.remove('opened');
    return true;
  };
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href]');
    if(!link) return;
    const url=new URL(link.href,location.href);
    if(url.pathname===location.pathname && jump(url.hash)) { event.preventDefault(); event.stopImmediatePropagation(); }
  },true);
  if(location.hash) window.addEventListener('load',()=>{ ScrollTrigger?.refresh(); jump(location.hash); },{once:true});
  document.querySelectorAll('[data-enquiry-service]').forEach(link => link.addEventListener('click', () => {
    const select = document.getElementById('ts-enquiry-service');
    if (select) { select.value = link.dataset.enquiryService; select.dispatchEvent(new Event('change',{bubbles:true})); }
  }));
})();
