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

const slideTargets = [...document.querySelectorAll('.slide-page .detail-hero, .slide-page .signal-section, .slide-page .prototype-slide, .slide-page .prototype-review, .slide-page .story-step, .slide-page .field-evidence, .slide-page .next-workspace')];
if (slideTargets.length) {
  document.documentElement.classList.add('slide-mode');
  slideTargets.forEach((section) => section.classList.add('slide-panel-target'));

  const slideNav = document.createElement('nav');
  slideNav.className = 'slide-nav';
  slideNav.setAttribute('aria-label', 'Page slides');
  const slideButtons = slideTargets.map((section, index) => {
    const button = document.createElement('button');
    const label = section.querySelector('.eyebrow, .step-number')?.textContent.trim() || `Slide ${index + 1}`;
    button.type = 'button';
    button.title = label;
    button.setAttribute('aria-label', `Go to ${label}`);
    button.addEventListener('click', () => section.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' }));
    slideNav.append(button);
    return button;
  });
  document.body.append(slideNav);

  const cue = document.createElement('div');
  cue.className = 'slide-cue';
  cue.textContent = 'SCROLL TO NEXT VIEW';
  document.body.append(cue);

  let activeSlide = 0;
  const setActiveSlide = (index) => {
    activeSlide = index;
    slideTargets.forEach((section, current) => section.classList.toggle('slide-active', current === index));
    slideButtons.forEach((button, current) => current === index ? button.setAttribute('aria-current', 'true') : button.removeAttribute('aria-current'));
    cue.textContent = index === slideTargets.length - 1 ? 'END OF PAGE' : 'SCROLL TO NEXT VIEW';
  };
  setActiveSlide(0);

  const slideObserver = new IntersectionObserver((entries) => {
    const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (visible) setActiveSlide(slideTargets.indexOf(visible.target));
  }, { threshold: [.35, .55, .72], rootMargin: '-12% 0px -12% 0px' });
  slideTargets.forEach((section) => slideObserver.observe(section));

  if (!reducedMotion && matchMedia('(pointer:fine)').matches) {
    const goToSlide = (direction) => {
      const next = Math.max(0, Math.min(slideTargets.length - 1, activeSlide + direction));
      if (next === activeSlide) return false;
      setActiveSlide(next);
      slideTargets[next].scrollIntoView({ behavior: 'smooth', block: 'start' });
      return true;
    };
    addEventListener('keydown', (event) => {
      if (!['ArrowDown', 'PageDown', 'ArrowUp', 'PageUp'].includes(event.key) || event.altKey || event.ctrlKey || event.metaKey) return;
      if (goToSlide(event.key === 'ArrowDown' || event.key === 'PageDown' ? 1 : -1)) event.preventDefault();
    });
  }
}
