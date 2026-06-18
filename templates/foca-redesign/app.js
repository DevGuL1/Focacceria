(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── THEME (dark / light) ──────────────────────────── */
  const THEME_KEY = 'foca-theme';
  const root = document.documentElement;
  const icons = { light: '🌿', dark: '☀️' };

  const applyTheme = (t) => {
    root.setAttribute('data-theme', t);
    localStorage.setItem(THEME_KEY, t);
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      btn.textContent = t === 'dark' ? icons.dark : icons.light;
      btn.setAttribute('aria-label', t === 'dark' ? 'ღია რეჟიმი' : 'ბნელი რეჟიმი');
    });
  };

  const saved = localStorage.getItem(THEME_KEY);
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(saved || (prefersDark ? 'dark' : 'light'));

  document.querySelectorAll('.theme-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
  });

  /* ── HEADER SHRINK ────────────────────────────────── */
  const header = document.querySelector('.header');
  const onScroll = () => {
    const y = window.scrollY || 0;
    if (header) header.classList.toggle('is-compact', y > 40);
    document.documentElement.style.setProperty('--bar-h', y > 40 ? '40px' : '50px');
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ── REVEAL ───────────────────────────────────────── */
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      }
    }, { threshold: 0.10 });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('is-visible'));
  }

  /* ── MEDIA SHELL ──────────────────────────────────── */
  const mediaShell = document.querySelector('.media-shell');
  if (mediaShell && 'IntersectionObserver' in window && !reduced) {
    const io2 = new IntersectionObserver((entries) => {
      for (const e of entries) { if (e.isIntersecting) mediaShell.classList.add('is-settled'); }
    }, { threshold: 0.22 });
    io2.observe(mediaShell);
  } else if (mediaShell) {
    mediaShell.classList.add('is-settled');
  }

  /* ── HERO PARALLAX ────────────────────────────────── */
  const heroBg = document.querySelector('.hero-bg');
  const parallax = () => {
    if (!heroBg || reduced) return;
    const rect = heroBg.getBoundingClientRect();
    const vh = window.innerHeight || 1;
    const t = Math.max(-1, Math.min(1, (rect.top - vh * 0.15) / (vh * 0.85)));
    const video = heroBg.querySelector('.hero-video');
    if (video) video.style.transform = `translateY(${t * 6}px) scale(1.0)`;
  };
  if (!reduced) window.addEventListener('scroll', parallax, { passive: true });

  /* ── ORDER MODAL ──────────────────────────────────── */
  const modal = document.querySelector('#orderModal');
  const open  = () => modal && modal.classList.add('is-open');
  const close = () => modal && modal.classList.remove('is-open');
  document.querySelectorAll('[data-open-order]').forEach(b => b.addEventListener('click', open));
  document.querySelectorAll('[data-close-order]').forEach(b => b.addEventListener('click', close));
  if (modal) {
    modal.addEventListener('click', e => { if (e.target.matches('.modal__backdrop')) close(); });
    window.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  /* ── MENU TABS ────────────────────────────────────── */
  const tabBtns   = Array.from(document.querySelectorAll('[data-tab]'));
  const tabPanels = Array.from(document.querySelectorAll('[data-panel]'));

  if (tabBtns.length) {
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-tab');
        tabBtns.forEach(b => { b.classList.remove('is-active'); b.setAttribute('aria-selected','false'); });
        btn.classList.add('is-active');
        btn.setAttribute('aria-selected','true');
        tabPanels.forEach(p => p.classList.toggle('is-active', p.getAttribute('data-panel') === target));
        /* re-trigger reveals inside newly shown panel */
        document.querySelectorAll('.tab-panel.is-active .reveal:not(.is-visible)').forEach(el => {
          el.classList.add('is-visible');
        });
      });
    });
  }

  /* ── MENU FILTER + SEARCH ─────────────────────────── */
  const searchInput = document.querySelector('[data-menu-search]');
  const filterBtns  = Array.from(document.querySelectorAll('[data-menu-filter]'));
  const items       = Array.from(document.querySelectorAll('[data-menu-item]'));

  if (items.length) {
    let active = 'ყველა';
    const norm = s => (s || '').toLowerCase().trim();

    const apply = () => {
      const q = norm(searchInput ? searchInput.value : '');
      items.forEach(el => {
        const name = norm(el.getAttribute('data-name'));
        const tags = norm(el.getAttribute('data-tags'));
        const passQ = !q || name.includes(q) || tags.includes(q);
        const passF = active === 'ყველა' || tags.split(',').map(t => t.trim()).includes(norm(active));
        el.style.display = (passQ && passF) ? '' : 'none';
      });
    };

    filterBtns.forEach(b => {
      b.addEventListener('click', () => {
        filterBtns.forEach(x => x.classList.remove('is-active'));
        b.classList.add('is-active');
        active = b.getAttribute('data-menu-filter') || 'ყველა';
        apply();
      });
    });
    if (searchInput) searchInput.addEventListener('input', apply);
    apply();
  }
})();
