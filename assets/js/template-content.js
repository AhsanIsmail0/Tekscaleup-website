/* Connect the template navigation to its existing GSAP smooth scroller. */
(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const menu = document.querySelector('.tp-offcanvas-area');
  const openButton = document.querySelector('.tp-offcanvas-open-btn');
  const closeButton = document.querySelector('.tp-offcanvas-close-btn');
  const overlay = document.querySelector('.body-overlay');
  const syncMenu = () => {
    const opened = menu?.classList.contains('opened') ?? false;
    if (menu) { menu.inert = !opened; menu.setAttribute('aria-hidden', String(!opened)); }
    openButton?.setAttribute('aria-expanded', String(opened));
  };
  const closeMenu = () => {
    menu?.classList.remove('opened');
    overlay?.classList.remove('opened');
    syncMenu();
  };
  if (menu) {
    menu.id = 'site-menu';
    openButton?.setAttribute('aria-controls', menu.id);
    new MutationObserver(syncMenu).observe(menu, { attributes: true, attributeFilter: ['class'] });
    syncMenu();
  }
  openButton?.addEventListener('click', () => {
    if (reducedMotion) { menu?.classList.add('opened'); overlay?.classList.add('opened'); }
    syncMenu();
    closeButton?.focus({ preventScroll: true });
  });
  closeButton?.addEventListener('click', () => { closeMenu(); openButton?.focus({ preventScroll: true }); });
  overlay?.addEventListener('click', closeMenu);
  document.addEventListener('keydown', event => {
    if (!menu?.classList.contains('opened')) return;
    if (event.key === 'Escape') { closeMenu(); openButton?.focus({ preventScroll: true }); }
    if (event.key !== 'Tab') return;
    const focusable = [...menu.querySelectorAll('a[href],button:not([disabled])')].filter(el => el.getClientRects().length);
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
  });
  if (reducedMotion) {
    const nav = document.querySelector('.tp-offcanvas-menu nav');
    const links = document.querySelector('.tp-mobile-menu-active > ul');
    if (nav && links && !nav.children.length) nav.append(links.cloneNode(true));
    document.querySelectorAll('[data-background]').forEach(el => { el.style.backgroundImage = `url("${el.dataset.background}")`; });
    document.querySelectorAll('[data-purecounter-end]').forEach(el => { el.textContent = el.dataset.purecounterEnd; });
    document.querySelector('#back_to_top')?.addEventListener('click', event => { event.preventDefault(); window.scrollTo({ top: 0, behavior: 'instant' }); });
    const back = document.querySelector('.back-to-top-wrapper');
    const updateBack = () => back?.classList.toggle('back-to-top-btn-show', window.scrollY > 300);
    window.addEventListener('scroll', updateBack, { passive: true });
    updateBack();
    document.querySelectorAll('.swiper').forEach(el => el.swiper?.autoplay?.stop());
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    const hash = link.getAttribute('href');
    if (hash.length < 2) return;
    const target = document.getElementById(hash.slice(1));
    if (!target) return;
    event.preventDefault();
    closeMenu();
    const smoother = window.ScrollSmoother?.get();
    if (smoother) smoother.scrollTo(target, true, 'top 100px');
    else target.scrollIntoView({ behavior: reducedMotion ? 'instant' : 'smooth', block: 'start' });
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  });
})();
