/* WANDER — original scroll-driven experiment by Meyene.
   Different depth planes move by different distances as a scene is scrolled.
   Kept dependency-free so it works directly on GitHub Pages. */
'use strict';

const scenes = [...document.querySelectorAll('.parallax-scene')];
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const progress = document.getElementById('page-progress-bar');
let ticking = false;
let pointerX = 0;
let pointerY = 0;

// Seeded generator keeps the particle positions consistent after refresh.
function randomSeed(seed) {
  return () => {
    seed = (Math.imul(1664525, seed) + 1013904223) >>> 0;
    return seed / 4294967296;
  };
}
const rand = randomSeed(19062026);

// Tiny independent points of light; no downloaded images or external libraries.
document.querySelectorAll('[data-stars]').forEach((container) => {
  const count = Number(container.dataset.stars);
  for (let i = 0; i < count; i++) {
    const star = document.createElement('i');
    star.className = 'star';
    const diameter = 1 + rand() * 2;
    Object.assign(star.style, {
      left: `${rand() * 100}%`, top: `${rand() * 75}%`,
      width: `${diameter}px`, height: `${diameter}px`,
      '--twinkle': `${3 + rand() * 5}s`, '--delay': `${-rand() * 7}s`
    });
    container.append(star);
  }
});

document.querySelectorAll('[data-particles]').forEach((container) => {
  for (let i = 0; i < Number(container.dataset.particles); i++) {
    const mote = document.createElement('i');
    mote.className = 'mote';
    Object.assign(mote.style, {
      left: `${8 + rand() * 84}%`, top: `${18 + rand() * 66}%`,
      '--duration': `${3.5 + rand() * 5}s`, '--delay': `${-rand() * 7}s`
    });
    container.append(mote);
  }
});

function render() {
  ticking = false;
  const maxScroll = Math.max(1, document.documentElement.scrollHeight - innerHeight);
  progress.style.width = `${(scrollY / maxScroll) * 100}%`;
  if (reducedMotion.matches) return;

  const compact = innerWidth < 760;
  for (const scene of scenes) {
    const bounds = scene.getBoundingClientRect();
    if (bounds.bottom < -100 || bounds.top > innerHeight + 100) continue;
    const distance = Math.max(0, bounds.height - innerHeight);
    const travelled = Math.min(distance, Math.max(0, -bounds.top));
    for (const layer of scene.querySelectorAll('.parallax-layer')) {
      const speed = Number(layer.dataset.speed || 0);
      const sideways = Number(layer.dataset.x || 0);
      const driftX = (compact ? 0 : pointerX * sideways * 30);
      const driftY = compact ? 0 : pointerY * Math.abs(speed) * 12;
      const y = travelled * speed + driftY;
      layer.style.transform = `translate3d(${driftX.toFixed(2)}px,${y.toFixed(2)}px,0)`;
    }
  }
}
function requestRender() {
  if (!ticking) {
    ticking = true;
    requestAnimationFrame(render);
  }
}
window.addEventListener('scroll', requestRender, { passive: true });
window.addEventListener('resize', requestRender);
window.addEventListener('pointermove', (event) => {
  if (event.pointerType === 'touch') return;
  pointerX = (event.clientX / innerWidth - .5) * 2;
  pointerY = (event.clientY / innerHeight - .5) * 2;
  requestRender();
}, { passive: true });
reducedMotion.addEventListener('change', () => {
  if (reducedMotion.matches) {
    document.querySelectorAll('.parallax-layer').forEach(layer => { layer.style.transform = ''; });
  }
  requestRender();
});

// Reveal editorial sections as they enter the viewport.
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { rootMargin: '0px 0px -12% 0px', threshold: .12 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
requestRender();
