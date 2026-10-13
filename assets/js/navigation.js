/* Keep the template's mobile accordion and add keyboard/click support on desktop. */
(() => {
  const nav = document.querySelector('.tp-header-menu .ts-navigation');
  if (!nav) return;
  const items = [...nav.querySelectorAll(':scope > .has-dropdown')];
  function close() { items.forEach(li => { li.classList.remove('ts-nav-open'); li.querySelector(':scope > a').setAttribute('aria-expanded','false'); }); }
  items.forEach(li => {
    const link = li.querySelector(':scope > a');
    link.addEventListener('click', e => { if(li.classList.contains('ts-nav-wide')) return; e.preventDefault(); const open = !li.classList.contains('ts-nav-open'); close(); li.classList.toggle('ts-nav-open',open); link.setAttribute('aria-expanded',String(open)); });
    li.addEventListener('mouseenter', () => link.setAttribute('aria-expanded','true'));
    li.addEventListener('mouseleave', () => { if (!li.classList.contains('ts-nav-open')) link.setAttribute('aria-expanded','false'); });
    li.addEventListener('focusin', () => link.setAttribute('aria-expanded','true'));
    li.addEventListener('focusout', e => { if (!li.contains(e.relatedTarget)) { li.classList.remove('ts-nav-open'); link.setAttribute('aria-expanded','false'); } });
  });
  document.addEventListener('click', e => { if (!nav.contains(e.target)) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { close(); if(nav.contains(document.activeElement)) document.activeElement.blur(); } });
  document.querySelectorAll('.tp-offcanvas-menu .tp-menu-close').forEach(button => { button.setAttribute('aria-label','Expand '+button.parentElement.querySelector('a').textContent.trim()); button.setAttribute('aria-expanded','false'); button.addEventListener('click',()=>button.setAttribute('aria-expanded',String(button.parentElement.classList.contains('active')))); });
})();
// Desktop exposes every sub-service; mobile uses native keyboard-accessible disclosures.
document.querySelectorAll('.tp-header-menu .ts-nav-service').forEach(group => {
  group.open = true;
  group.querySelector('summary').addEventListener('click', event => event.preventDefault());
});
document.querySelectorAll('.tp-offcanvas-menu .ts-nav-service').forEach(group => {
  group.open = false;
  group.addEventListener('toggle', () => {
    if (group.open) group.closest('.ts-service-groups').querySelectorAll('details').forEach(other => {
      if (other !== group) other.open = false;
    });
  });
});

// On touch devices the separate plus button expands Services; its text link navigates.
document.querySelectorAll('.tp-offcanvas-menu .ts-nav-wide > a').forEach(link => {
  link.addEventListener('click', event => { event.stopImmediatePropagation(); location.href=link.href; }, true);
});

// main.js deliberately skips animation setup for reduced motion; keep navigation usable.
if(matchMedia('(prefers-reduced-motion: reduce)').matches){
 document.querySelectorAll('.tp-offcanvas-menu .has-dropdown').forEach(item=>{
  const panel=item.querySelector(':scope > .ts-nav-panel');if(!panel||item.querySelector(':scope > .tp-menu-close'))return;
  const button=document.createElement('button');button.className='tp-menu-close';button.textContent='+';
  button.setAttribute('aria-label','Expand '+item.querySelector(':scope > a').textContent.trim());button.setAttribute('aria-expanded','false');
  button.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(open));panel.style.display=open?'block':'none';item.classList.toggle('active',open);});item.append(button);
 });
}
