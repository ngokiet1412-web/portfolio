(() => {
  if (typeof window.gtag !== 'function') return;

  document.addEventListener('click', (event) => {
    const link = event.target.closest('a');
    if (!link) return;

    const rawHref = link.getAttribute('href') || '';
    const linkText = link.textContent.trim().replace(/\s+/g, ' ').slice(0, 80);
    const pagePath = location.pathname;

    if (/\.pdf(?:$|[?#])/i.test(rawHref)) {
      gtag('event', 'cv_open', {
        page_path: pagePath,
        link_text: linkText,
        open_mode: link.hasAttribute('download') ? 'download' : 'view'
      });
      return;
    }

    if (rawHref.startsWith('mailto:') || rawHref.startsWith('tel:')) {
      gtag('event', 'contact_click', {
        page_path: pagePath,
        contact_method: rawHref.startsWith('mailto:') ? 'email' : 'phone'
      });
      return;
    }

    try {
      const url = new URL(link.href, location.href);
      if (url.hostname === 'github.com') {
        gtag('event', 'github_click', {
          page_path: pagePath,
          link_text: linkText
        });
      }
    } catch (_) {
      // Ignore malformed or browser-generated URLs.
    }
  }, { capture: true });
})();
