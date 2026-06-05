(function () {
  'use strict';

  // ── Classes globales ────────────────────────────────────────
  document.documentElement.classList.add('js-ready');

  const body   = document.body;
  const header = document.querySelector('[data-header]');
  const toggle = document.querySelector('.nav-toggle');
  const nav    = document.querySelector('.site-nav');

  // ── Header scroll state ────────────────────────────────────
  function setHeaderState() {
    if (!header) return;
    const scrolled = window.scrollY > 32;
    header.classList.toggle('scrolled', scrolled);
  }
  setHeaderState();
  window.addEventListener('scroll', setHeaderState, { passive: true });

  // ── Hero image parallax légère + loaded class ───────────────
  const hero = document.querySelector('.hero');
  if (hero) {
    const heroBgImg = hero.querySelector('.hero-bg img');
    if (heroBgImg) {
      if (heroBgImg.complete) {
        hero.classList.add('loaded');
      } else {
        heroBgImg.addEventListener('load', () => hero.classList.add('loaded'));
      }
    }
  }

  // ── Menu burger ────────────────────────────────────────────
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = !body.classList.contains('menu-open');
      body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
    });

    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });

    // Fermer avec Escape
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && body.classList.contains('menu-open')) {
        body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  // ── Reveal (IntersectionObserver) ──────────────────────────
  const revealItems = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealItems.length) {
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -6% 0px' }
    );
    revealItems.forEach(item => observer.observe(item));
  } else {
    revealItems.forEach(item => item.classList.add('is-visible'));
  }

  // ── Page transitions (View Transitions API) ─────────────────
  if ('startViewTransition' in document) {
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href');
      // Uniquement les liens internes (pages du site)
      if (
        href &&
        !href.startsWith('http') &&
        !href.startsWith('mailto') &&
        !href.startsWith('tel') &&
        !href.startsWith('#') &&
        href.endsWith('.html')
      ) {
        link.addEventListener('click', e => {
          e.preventDefault();
          document.startViewTransition(() => {
            window.location.href = href;
          });
        });
      }
    });
  }

  // ── Mise en évidence du lien nav actif (basé sur l'URL) ────
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.site-nav a').forEach(link => {
    const linkPath = link.getAttribute('href').split('/').pop();
    if (linkPath === currentPath) {
      link.setAttribute('aria-current', 'page');
    }
  });

})();
