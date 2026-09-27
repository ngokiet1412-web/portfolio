const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

const revealElements = document.querySelectorAll('.reveal');
if (!reducedMotion && 'IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  }, { threshold: 0.08 });
  revealElements.forEach((element) => revealObserver.observe(element));
} else {
  revealElements.forEach((element) => element.classList.add('visible'));
}

const progressBar = document.getElementById('bar');
function updateProgress() {
  const maximum = document.documentElement.scrollHeight - innerHeight;
  if (progressBar) progressBar.style.height = `${maximum > 0 ? (scrollY / maximum) * 100 : 0}%`;
}
addEventListener('scroll', updateProgress, { passive: true });
updateProgress();

const navLinks = [...document.querySelectorAll('.top nav a')];
const sections = [...document.querySelectorAll('main section[id]')];
if ('IntersectionObserver' in window) {
  const navObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      navLinks.forEach((link) => link.removeAttribute('aria-current'));
      navLinks.find((link) => link.hash === `#${entry.target.id}`)?.setAttribute('aria-current', 'true');
    }
  }, { rootMargin: '-35% 0px -55% 0px' });
  sections.forEach((section) => navObserver.observe(section));
}

const workflowData = {
  nx: {
    eyebrow: 'SIEMENS NX / CAPTURED WORKSPACE',
    title: 'From interface requirements to editable geometry.',
    intro: 'One local NX capture is presented as three focused views: the full workspace, Assembly Navigator and modeled assembly.',
    image: 'assets/nx.webp',
    views: [['contain', 'Full NX workspace'], ['zoom-left', 'Assembly Navigator'], ['zoom-center', '3D assembly focus']],
    steps: [
      ['01', 'Define interfaces', 'Envelope, mounting points, clearances and service access.'],
      ['02', 'Build or import', 'Create parts or handle STEP, Parasolid and NX geometry.'],
      ['03', 'Assemble', 'Place components and apply relationships or constraints.'],
      ['04', 'Inspect', 'Review fit, packaging and accessible interfaces.'],
      ['05', 'Revise', 'Update geometry when field or analysis findings change.'],
      ['06', 'Handoff', 'Keep model structure usable for CAE and documentation.']
    ]
  },
  ansys: {
    eyebrow: 'ANSYS MECHANICAL / CAPTURED WORKSPACE',
    title: 'Turn the CAD model into an engineering question.',
    intro: 'The Mechanical capture is separated into full-workspace, model-tree and contour-result views while keeping assumptions and interpretation explicit.',
    image: 'assets/ansys.webp',
    views: [['contain', 'Full Mechanical workspace'], ['zoom-left', 'Outline and setup'], ['zoom-center', 'Result contour focus']],
    steps: [
      ['01', 'Define question', 'Choose the risk or response that needs evaluation.'],
      ['02', 'Prepare model', 'Simplify geometry and define relevant contacts.'],
      ['03', 'Assign inputs', 'Material, supports, loads or thermal conditions.'],
      ['04', 'Mesh', 'Use a mesh appropriate to geometry and purpose.'],
      ['05', 'Solve and inspect', 'Read stress, deformation or temperature fields.'],
      ['06', 'Iterate', 'Revise assumptions or geometry and check again.']
    ]
  }
};

const dialog = document.getElementById('workflow-dialog');
const dialogContent = document.getElementById('dialog-content');
function openWorkflow(key) {
  const data = workflowData[key];
  if (!data || !dialog || !dialogContent) return;
  dialogContent.innerHTML = `
    <div class="dialog-inner">
      <header class="dialog-head"><p class="eyebrow">${data.eyebrow}</p><h2 id="dialog-title">${data.title}</h2><p>${data.intro}</p></header>
      <div class="focus-gallery">${data.views.map(([className, label]) => `<figure class="focus-shot ${className}"><img src="${data.image}" alt="${label}"><figcaption>${label}</figcaption></figure>`).join('')}</div>
      <div class="process-list">${data.steps.map(([number, title, text]) => `<article><span>${number}</span><h3>${title}</h3><p>${text}</p></article>`).join('')}</div>
    </div>`;
  dialog.showModal();
  document.body.style.overflow = 'hidden';
}

document.querySelectorAll('[data-workflow]').forEach((button) => button.addEventListener('click', () => openWorkflow(button.dataset.workflow)));
document.querySelector('.dialog-close')?.addEventListener('click', () => dialog?.close());
dialog?.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
dialog?.addEventListener('close', () => { document.body.style.overflow = ''; });

if (!reducedMotion && matchMedia('(pointer:fine)').matches) {
  document.querySelectorAll('.tilt').forEach((card) => {
    card.addEventListener('pointermove', (event) => {
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      card.style.setProperty('--ry', `${x * 2.2}deg`);
      card.style.setProperty('--rx', `${y * -2.2}deg`);
    });
    card.addEventListener('pointerleave', () => {
      card.style.setProperty('--ry', '0deg');
      card.style.setProperty('--rx', '0deg');
    });
  });
}
