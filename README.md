# WANDER — Interactive Parallax Experience

An original, responsive, scroll-driven journey through dawn, the forest canopy and the night sky. Created by **Ating Meyene-Abasi Wesley Abang (Meyene)** for the LimeLightR Parallax Scrolling assignment.

## What it demonstrates

- Three original full-screen environments: **First Light**, **The Canopy**, and **After Dark**.
- Over 30 independent scenery, atmosphere and animation layers in total.
- Vanilla JavaScript parallax animation: each element has a `data-speed` value; JavaScript calculates its offset from the section's scroll progress and uses `translate3d`.
- Extra depth from clouds, mist, sun/moon glow, trees, forest light shafts, fireflies, stars and moving birds.
- Subtle mouse-following motion on desktop.
- Editorial storytelling sections, a replay link and a scroll progress bar.
- Small-screen layouts, accessible semantic HTML, and respect for `prefers-reduced-motion`.
- No npm, build step, external libraries, CDNs, or external image dependencies.

## How to run

Open `index.html` in a browser. Scroll to see the separate layers move at different speeds. For a local web server, run `python -m http.server 8000` in this folder and visit http://localhost:8000.

## How the JS works

1. The `.parallax-scene` sections are tall (`170vh`), while `.scene-sticky` pins the scene at `100vh` during a scroll.
2. Every element marked `.parallax-layer` has its own `data-speed` value (small numbers for distant scenery, larger numbers for foreground objects).
3. In `js/main.js`, `render()` computes the scroll distance travelled inside the current scene and translates each layer by `travelled * data-speed`.
4. A passive scroll listener schedules a single `requestAnimationFrame` to keep updates smooth. On reduced-motion devices the effects are disabled.
5. Star and mote elements are generated with seeded randomness in JS, so the details stay visually consistent.

You can experiment by changing the `data-speed` attributes in `index.html` or the illustration colors in `assets/*.svg`.

## Publish with GitHub Pages

1. Create a **new public repository**, for example `wander-parallax-task2` (separate from your first-task `responsive-portfolio` repository).
2. Upload the *contents of this folder*, including `index.html`, `css`, `js` and `assets`, directly to the repository **root**. Do not upload the enclosing `Meyene_Parallax_Task2` folder as an extra directory.
3. Go to **Settings → Pages**. Choose **Deploy from a branch → main → / (root)**, then Save.
4. Once the site reports *Your site is live*, check `https://YOUR-USERNAME.github.io/wander-parallax-task2/`.
5. Submit the **live .github.io link** as requested. Optionally include the source repository link.

## Attribution

All landscape SVG assets and code were created specifically for this original project. The site is not a copy of the starter or the Moooi example. No third-party images were used.
