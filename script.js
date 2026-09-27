const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

addEventListener('pageshow', () => document.body.classList.remove('is-leaving'));
document.addEventListener('click', (event) => {
  const link = event.target.closest('a');
  if (!link || event.defaultPrevented || event.button !== 0 || link.target || link.hasAttribute('download')) return;
  const url = new URL(link.href, location.href);
  if (url.origin !== location.origin || url.pathname === location.pathname && url.hash) return;
  if (!/\.html$|\/$/.test(url.pathname)) return;
  if (reducedMotion) return;
  event.preventDefault();
  document.body.classList.add('is-leaving');
  setTimeout(() => { location.href = url.href; }, 280);
});

const staggerGroups = document.querySelectorAll('.signal-chain, .review-grid, .discipline-grid, .field-preview-grid, .workflow-flow');
staggerGroups.forEach((group) => [...group.children].forEach((element, index) => {
  element.classList.add('motion-item');
  element.style.setProperty('--motion-delay', `${Math.min(index * 70, 210)}ms`);
}));
document.querySelectorAll('.story-step, .evidence-note, .portfolio-board, .next-workspace').forEach((element) => element.classList.add('motion-item'));

const revealElements = document.querySelectorAll('.reveal, .motion-item');
document.querySelector('.hero, .detail-hero')?.classList.add('visible');
if (!reducedMotion && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries, currentObserver) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('visible');
      currentObserver.unobserve(entry.target);
    }
  }, { threshold: 0.08, rootMargin: '0px 0px -7% 0px' });
  revealElements.forEach((element) => observer.observe(element));
} else revealElements.forEach((element) => element.classList.add('visible'));

const progressBar = document.getElementById('bar');
let scrollFrame = 0;
function updateProgress() {
  const maximum = document.documentElement.scrollHeight - innerHeight;
  if (progressBar) progressBar.style.height = `${maximum > 0 ? scrollY / maximum * 100 : 0}%`;
  if (!reducedMotion) document.documentElement.style.setProperty('--scroll-shift', `${Math.max(-30, scrollY * -.018)}`);
  scrollFrame = 0;
}
addEventListener('scroll', () => {
  if (!scrollFrame) scrollFrame = requestAnimationFrame(updateProgress);
}, { passive: true });
updateProgress();

const navLinks = [...document.querySelectorAll('.top nav a[href^="#"]')];
const sections = [...document.querySelectorAll('main section[id]')];
if ('IntersectionObserver' in window && navLinks.length) {
  const navObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      navLinks.forEach((link) => link.removeAttribute('aria-current'));
      navLinks.find((link) => link.hash === `#${entry.target.id}`)?.setAttribute('aria-current', 'true');
    }
  }, { rootMargin: '-35% 0px -55% 0px' });
  sections.forEach((section) => navObserver.observe(section));
}

if (!reducedMotion && matchMedia('(pointer:fine)').matches) {
  document.querySelectorAll('.tilt').forEach((card) => {
    card.addEventListener('pointermove', (event) => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty('--ry', `${((event.clientX - rect.left) / rect.width - .5) * 1.8}deg`);
      card.style.setProperty('--rx', `${((event.clientY - rect.top) / rect.height - .5) * -1.8}deg`);
    });
    card.addEventListener('pointerleave', () => { card.style.setProperty('--ry', '0deg'); card.style.setProperty('--rx', '0deg'); });
  });
}
