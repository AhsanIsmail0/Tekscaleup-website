(() => {
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.querySelector('#mobile-navigation');
  const closeMenu = () => {
    menu.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation');
    document.body.classList.remove('menu-open');
  };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    menu.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    document.body.classList.toggle('menu-open', open);
  });
  menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !menu.hidden) {
      closeMenu();
      toggle.focus();
    }
  });
  window.matchMedia('(min-width: 768px)').addEventListener('change', event => {
    if (event.matches) closeMenu();
  });
  const filterButtons = document.querySelectorAll('[data-project-filter]');
  const cards = document.querySelectorAll('[data-project-category]');
  const status = document.querySelector('#project-status');
  filterButtons.forEach(button => button.addEventListener('click', () => {
    const filter = button.dataset.projectFilter;
    filterButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    cards.forEach(card => {
      card.hidden = filter !== 'all' && card.dataset.projectCategory !== filter;
      if (!card.hidden) count++;
    });
    status.textContent = `${count} ${count === 1 ? 'project' : 'projects'} shown`;
  }));
})();
