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
    else if (window.gsap && !reducedMotion) window.gsap.to(window, {scrollTo: {y: target, offsetY: 100, autoKill: true}, duration: .85, ease: 'power2.inOut', overwrite: 'auto'});
    else target.scrollIntoView({ behavior: 'instant', block: 'start' });
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  });
})();

/* A finite assembly tells the brand story; the first scroll hands off to About. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hero = document.querySelector('.ts-brand-hero');
  if (hero && window.gsap && !reduce) {
    const pieces = hero.querySelectorAll('.ts-assembly-piece');
    const timeline = gsap.timeline({delay: .3});
    timeline.from(pieces[2], {opacity: 0, scale: .4, transformOrigin: 'center', duration: .55, ease: 'power2.out'});
    timeline.from(pieces[0], {x: -16, y: -10, opacity: 0, duration: .9, ease: 'power3.out'}, .35);
    timeline.from(pieces[1], {x: 16, y: 10, opacity: 0, duration: .9, ease: 'power3.out'}, .55);
    timeline.from(hero.querySelectorAll('.ts-brand-disciplines span'), {opacity: 0, y: 8, stagger: .12, duration: .5}, 1);
    gsap.to(hero.querySelector('.ts-assembly-guides'), {opacity: .15, scrollTrigger: {trigger: '.ts-hero', start: 'top top', end: 'bottom 20%', scrub: true}});
  }
  const form = document.querySelector('#ts-enquiry-form');
  if (!form) return;
  const link = form.querySelector('.ts-enquiry-action a');
  const updateDraft = () => {
    const name = form.elements.name.value.trim();
    const service = form.elements.service.value;
    const brief = form.elements.brief.value.trim();
    const body = `Hello TekScaleUp,\n\nI'm interested in ${service}.\n\n${brief || 'My project goals:'}\n\n${name ? 'Name: ' + name : ''}`;
    link.href = `mailto:contact@tekscaleup.com?subject=${encodeURIComponent('Project enquiry: ' + service)}&body=${encodeURIComponent(body)}`;
  };
  form.addEventListener('input', updateDraft);
  form.addEventListener('change', updateDraft);
  form.addEventListener('submit', event => {event.preventDefault(); updateDraft(); link.click();});
  link.addEventListener('click', () => {document.querySelector('#ts-enquiry-status').textContent = 'Your email app will open a draft. Nothing has been sent by this website. If it does not open, email contact@tekscaleup.com directly.';});
  updateDraft();
})();
/* Scroll-driven mobile stacks; desktop panels remain owned by main.js. */
(() => {
  if (!window.gsap || !window.ScrollTrigger) return;
  const media = gsap.matchMedia();
  media.add('(max-width: 767px) and (prefers-reduced-motion: no-preference)', () => {
    const stage = document.querySelector('#services .tp-service-pin');
    const panels = stage ? [...stage.querySelectorAll('.tp-service-item')] : [];
    let height = 0;
    let headingStep = 54;
    const measure = () => {
      panels.forEach(panel => { panel.style.minHeight = ''; });
      const cardHeight = Math.max(...panels.map(panel => panel.scrollHeight), 0);
      panels.forEach(panel => { panel.style.minHeight = `${cardHeight}px`; });
      headingStep = Math.max(54, ...panels.map(panel => Math.ceil(panel.querySelector(".tp-section-title").getBoundingClientRect().height + 8)));
      height = cardHeight + (panels.length - 1) * headingStep;
      if (stage) stage.style.height = `${height}px`;
    };
    if (stage && panels.length) {
      stage.classList.add('ts-mobile-service-stage');
      panels.forEach((panel, i) => { panel.style.zIndex = i + 1; });
      measure();
      const story = gsap.timeline({scrollTrigger: {
        trigger: stage, start: () => `top ${Math.min(80, innerHeight - height - 20)}px`,
        end: () => `+=${Math.max(innerHeight * .8, height) * (panels.length - 1)}`,
        pin: true, scrub: .35, invalidateOnRefresh: true, onRefreshInit: measure
      }});
      panels.slice(1).forEach((panel, i) => {
        story.fromTo(panel, {y: () => height}, {y: () => (i + 1) * headingStep, duration: 1, ease: 'none'});
        story.to({}, {duration: .3});
      });
    }
    const grid = document.querySelector('#projects .ts-project-grid');
    const cards = grid ? [...grid.children] : [];
    grid?.classList.add('ts-mobile-project-stack');
    cards.forEach((card, i) => {
      card.style.zIndex = i + 1;
      if (i === cards.length - 1) return;
      ScrollTrigger.create({trigger: card, start: 'top 80px', endTrigger: cards[cards.length - 1],
        end: 'top 80px', pin: card, pinSpacing: false, invalidateOnRefresh: true});
    });
    return () => {
      stage?.classList.remove('ts-mobile-service-stage');
      if (stage) stage.style.height = '';
      panels.forEach(panel => { panel.style.zIndex = ''; panel.style.minHeight = ''; });
      grid?.classList.remove('ts-mobile-project-stack');
      cards.forEach(card => { card.style.zIndex = ''; });
    };
  });
  document.fonts?.ready.then(() => ScrollTrigger.refresh());
})();
