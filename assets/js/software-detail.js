(() => {
  const select=document.getElementById('ts-enquiry-service');
  if(select) {select.value=document.body.dataset.service || 'Startup & Scaleup Services';select.dispatchEvent(new Event('change',{bubbles:true}));}
  document.querySelectorAll('.ts-detail-faq details').forEach(item=>item.addEventListener('toggle',()=>window.ScrollTrigger?.refresh()));
  if(window.gsap && !matchMedia('(prefers-reduced-motion: reduce)').matches){
    document.querySelectorAll('.ts-detail-capability-list article,.ts-detail-principles article').forEach(item=>gsap.from(item,{y:20,opacity:0,duration:.55,scrollTrigger:{trigger:item,start:'top 90%',once:true}}));
  }
})();
