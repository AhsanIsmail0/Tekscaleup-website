(() => {
 const section=document.querySelector('.ts-roadmap');if(!section)return;
 const path=section.querySelector('.ts-roadmap-progress'),steps=[...section.querySelectorAll('[data-roadmap-step]')],nodes=[...section.querySelectorAll('[data-roadmap-node]')];
 const length=path.getTotalLength();path.style.strokeDasharray=length;
 const fractions=nodes.map(node=>{const x=+node.getAttribute('cx'),y=+node.getAttribute('cy');let best=0,distance=Infinity;for(let i=0;i<=1200;i++){const p=path.getPointAtLength(length*i/1200),d=(p.x-x)**2+(p.y-y)**2;if(d<distance){distance=d;best=i/1200}}return best;});
 function render(progress,forced){path.style.strokeDashoffset=length*(1-progress);const point=path.getPointAtLength(length*progress);section.querySelectorAll('.ts-roadmap-marker,.ts-roadmap-marker-halo').forEach(node=>{node.setAttribute('cx',point.x);node.setAttribute('cy',point.y)});let active=forced??fractions.reduce((current,value,i)=>progress+.001>=value?i:current,0);steps.forEach((step,i)=>{step.classList.toggle('is-active',i===active);step.classList.toggle('is-reached',i<=active);if(i===active)step.setAttribute('aria-current','step');else step.removeAttribute('aria-current');nodes[i].classList.toggle('is-reached',i<=active)});section.querySelector('[data-roadmap-count]').textContent=`0${active+1} / 06`;}
 if(!window.gsap||!window.ScrollTrigger||matchMedia('(prefers-reduced-motion: reduce)').matches){render(1);steps.forEach(step=>step.classList.add('is-reached'));return;}
 // Geometry sync also handles scroll restoration and programmatic anchor jumps.
 let previous=-1,frame=0;
 function sync(){
  if(document.hidden)return;
  const bounds=section.getBoundingClientRect();
  if(bounds.top>innerHeight+150||bounds.bottom< -150){frame=requestAnimationFrame(sync);return;}
  if(matchMedia('(min-width:1200px)').matches){
   const spacer=section.parentElement.classList.contains('pin-spacer')?section.parentElement:null;
   const rect=(spacer||section).getBoundingClientRect();
   const travel=spacer?Math.max(1,spacer.offsetHeight-section.offsetHeight):Math.max(1,section.offsetHeight+innerHeight*.45);
   const p=Math.max(0,Math.min(1,((spacer?85:innerHeight*.7)-rect.top)/travel));
   if(Math.abs(p-previous)>.0001){render(p);previous=p;}
  }else{
   let active=0;steps.forEach((step,i)=>{if(step.getBoundingClientRect().top<innerHeight*.72)active=i;});
   if(active!==previous){render(fractions[active],active);previous=active;}
  }
  if(!document.hidden)frame=requestAnimationFrame(sync);
 }
 requestAnimationFrame(sync);
 document.addEventListener('visibilitychange',()=>{cancelAnimationFrame(frame);if(!document.hidden)sync();});
 const media=gsap.matchMedia();
 window.addEventListener('load',()=>ScrollTrigger.refresh(),{once:true});
 document.fonts?.ready.then(()=>ScrollTrigger.refresh());
 media.add('(min-width:1200px)',()=>{render(0);ScrollTrigger.create({trigger:section,start:'top 85px',end:()=>'+='+Math.max(1100,innerHeight*1.8),pin:section.offsetHeight<innerHeight-85,invalidateOnRefresh:true});});
 media.add('(max-width:1199px)',()=>{previous=-1;render(0);});
})();

