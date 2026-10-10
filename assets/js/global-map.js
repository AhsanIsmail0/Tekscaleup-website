/* Local SVG map. No map service, API keys or tracking required. */
(() => {
  const section = document.querySelector('#global-presence');
  if (!section) return;
  const locations = {
    pakistan: { country: 'Pakistan', cities: 'Lahore' },
    canada: { country: 'Canada', cities: 'Calgary & Edmonton' },
    japan: { country: 'Japan', cities: 'Chiba' }
  };
  const controls = [...section.querySelectorAll('[data-location]')];
  const detail = section.querySelector('#ts-map-detail');
  let selected = 'pakistan';
  const select = (key, automatic = false) => {
    // Scroll changes remain silent; deliberate selection announces the location.
    detail.setAttribute('aria-live', automatic ? 'off' : 'polite');
    if (!locations[key] || key === selected) return;
    selected = key;
    controls.forEach(control => {
      const active = control.dataset.location === key;
      control.classList.toggle('is-active', active);
      control.setAttribute('aria-pressed', String(active));
    });
    section.querySelector('[data-map-country]').textContent = locations[key].country;
    section.querySelector('[data-map-cities]').textContent = locations[key].cities;
  };
  controls.forEach(control => {
    control.addEventListener('click', () => select(control.dataset.location));
    control.addEventListener('focus', () => select(control.dataset.location));
    control.addEventListener('pointermove', event => {
      if (event.pointerType === 'mouse') select(control.dataset.location);
    });
    if (control.tagName.toLowerCase() === 'g') {
      control.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          select(control.dataset.location);
        }
      });
    }
  });
  const buttons = [...section.querySelectorAll('.ts-location-button')];
  buttons.forEach((button, index) => button.addEventListener('keydown', event => {
    const offset = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0;
    if (!offset) return;
    event.preventDefault();
    buttons[(index + offset + buttons.length) % buttons.length].focus({ preventScroll: true });
  }));

  if (!window.gsap || !window.ScrollTrigger) return;
  const gsap = window.gsap;
  const media = gsap.matchMedia();
  media.add({
    desktop: '(min-width: 992px) and (min-height: 700px)',
    small: '(max-width: 991px), (max-height: 699px)',
    reduce: '(prefers-reduced-motion: reduce)'
  }, context => {
    const showComplete = () => {
      section.querySelectorAll('.ts-map-country').forEach(country => country.classList.add('is-reached'));
      return () => section.querySelectorAll('.ts-map-country').forEach(country => country.classList.remove('is-reached'));
    };
    if (context.conditions.reduce) return showComplete();
    if (!context.conditions.desktop) {
      // No pinning or route sequence on smaller screens.
      gsap.from(section.querySelector('.ts-map-canvas'), {
        autoAlpha: 0, y: 18, duration: .65, ease: 'power2.out',
        scrollTrigger: { trigger: section, start: 'top 85%', once: true }
      });
      return showComplete();
    }
    section.classList.add('has-map-story');
    const order = ['pakistan', 'canada', 'japan'];
    const countries = order.map(key => section.querySelector(`.ts-map-country[data-location="${key}"]`));
    const routes = ['canada', 'japan'].map(key => section.querySelector(`[data-route="${key}"]`));
    const cities = buttons.map(button => button.querySelector('span:nth-child(2) > span'));
    routes.forEach(route => {
      const length = route.getTotalLength();
      gsap.set(route, { strokeDasharray: length, strokeDashoffset: length, opacity: .85 });
    });
    const story = { step: 0 };
    let lastStep = -1;
    const syncStep = () => {
      const step = Math.round(story.step);
      if (step === lastStep) return;
      lastStep = step;
      countries.forEach((country, index) => country.classList.toggle('is-reached', index <= step));
      select(order[Math.min(step, 2)], true);
    };
    const timeline = gsap.timeline({
      scrollTrigger: {
        id: 'tekscaleup-map-story', trigger: section,
        start: 'top 80px', end: () => `+=${window.innerHeight}`,
        pin: true, scrub: .6, anticipatePin: 1, invalidateOnRefresh: true
      },
      onUpdate: syncStep
    });
    timeline.fromTo(section.querySelector('.ts-map-canvas'), { autoAlpha: .15, y: 20 }, { autoAlpha: 1, y: 0, duration: .2 });
    timeline.fromTo(cities[0], { autoAlpha: .25 }, { autoAlpha: 1, duration: .12 }, 0);
    timeline.fromTo(cities[1], { autoAlpha: .25 }, { autoAlpha: 1, duration: .12 }, .42);
    timeline.fromTo(cities[2], { autoAlpha: .25 }, { autoAlpha: 1, duration: .12 }, .75);
    timeline.to(routes[0], { strokeDashoffset: 0, duration: .3, ease: 'none' }, .16);
    timeline.to(story, { step: 1, duration: .001 }, .46);
    timeline.to(routes[1], { strokeDashoffset: 0, duration: .27, ease: 'none' }, .5);
    timeline.to(story, { step: 2, duration: .001 }, .77);
    timeline.to({}, { duration: .23 });
    syncStep();
    return () => {
      section.classList.remove('has-map-story');
      countries.forEach(country => country.classList.remove('is-reached'));
      select('pakistan', true);
    };
  });
  // Font metrics can change pin geometry after initial parsing.
  document.fonts?.ready.then(() => window.ScrollTrigger.refresh());
})();
