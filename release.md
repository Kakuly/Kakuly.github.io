---
layout: page
title: Release
permalink: /release/
---

Release - 作品集

<div class="filter-section">
  <div class="filter-label">Artist:</div>
  <div id="artist-filter" class="filter-wrapper"></div>
  <div class="filter-label">Tags:</div>
  <div id="tag-filter" class="filter-wrapper"></div>
</div>

<div class="video-grid" id="video-grid">

<div class="video-item size-mid" data-tags="Release,EP,Music" data-artist="Kakuly">
  <a href="https://big-up.style/21Wcz2jUF8" target="_blank" class="video-link">
    <img src="https://i9.ytimg.com/s_p/OLAK5uy_mJlf5VGWY5BLOE9qdiwONY2lvvPEaSl8c/maxresdefault.jpg?sqp=COyby8sGir7X7AMICJv9_MoGEAE=&rs=AOn4CLCf-LUaCfhefvq0A23U0_ggmkV7iw&v=1767849627" alt="Release New EP &quot;snowflaking&quot;" class="video-thumbnail" loading="lazy">
  </a>
  <h3 class='video-title'>Release New EP &quot;snowflaking&quot;</h3>
  <p class='video-artist'>Kakuly</p>
  <p class='video-date'>2025-12-26</p>
  <div class="tag-container"><span class="work-tag">Release</span><span class="work-tag">EP</span><span class="work-tag">Music</span></div>
</div>

<div class="video-item size-mid" data-tags="Release,Album,Music" data-artist="Kakuly">
  <a href="https://big-up.style/AwGSfnO9I3" target="_blank" class="video-link">
    <img src="https://i9.ytimg.com/s_p/OLAK5uy_kN_SOIxifwhCGm4OMSaQY8ycqXmIzFkEc/maxresdefault.jpg?sqp=CNj4yssGir7X7AMICPm06cUGEAE=&rs=AOn4CLDd88RNpgoiSNJTKxAUe75cnL2kJQ&v=1757043321" alt="Release New Album &quot;DIRECT &amp; LOOP&quot;" class="video-thumbnail" loading="lazy">
  </a>
  <h3 class='video-title'>Release New Album &quot;DIRECT &amp; LOOP&quot;</h3>
  <p class='video-artist'>Kakuly</p>
  <p class='video-date'>2025-08-05</p>
  <div class="tag-container"><span class="work-tag">Release</span><span class="work-tag">Album</span><span class="work-tag">Music</span></div>
</div>

<div class="video-item size-mid" data-tags="Release,Album,Music" data-artist="Kakuly">
  <a href="https://big-up.style/Rfjwgu1vFD" target="_blank" class="video-link">
    <img src="https://i9.ytimg.com/s_p/OLAK5uy_nZcJam8ma9bN_41_S6VnsyXdzWlH6EAWs/maxresdefault.jpg?sqp=COyby8sGir7X7AMICNzvm70GEAE=&rs=AOn4CLBAZBEEEiMSsYwYLj0-1gRTOUS-3w&v=1738995676" alt="Release New Album &quot;Everything /// (to break me)&quot;" class="video-thumbnail" loading="lazy">
  </a>
  <h3 class='video-title'>Release New Album &quot;Everything /// (to break me)&quot;</h3>
  <p class='video-artist'>Kakuly</p>
  <p class='video-date'>2024-12-30</p>
  <div class="tag-container"><span class="work-tag">Release</span><span class="work-tag">Album</span><span class="work-tag">Music</span></div>
</div>

</div>
<div id="iris-in"></div><div id="iris-out"></div>

<style>
.filter-section { margin-bottom: 40px; }
.filter-label { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 0.7rem; text-transform: uppercase; opacity: 0.5; margin-bottom: 8px; margin-top: 15px; }
.filter-wrapper { display: flex; flex-wrap: wrap; gap: 10px; }
.filter-btn { cursor: pointer; font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; font-size: 0.8rem; padding: 5px 14px; border-radius: 20px; border: 1px solid var(--text-color); background: transparent; color: var(--text-color); transition: all 0.3s ease; text-transform: uppercase; opacity: 0.3; }
.filter-btn.active { opacity: 1; background: var(--text-color); color: var(--bg-color); }
.video-grid { display: grid !important; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)) !important; gap: 60px 40px !important; grid-auto-flow: dense; }
.video-item { transition: opacity 0.4s ease, transform 0.4s ease; backface-visibility: hidden; }
.video-item.size-mid { grid-column: span 2; grid-row: span 2; }
.video-item.size-max { grid-column: span 3; grid-row: span 2; }
@media screen and (max-width: 900px) { .video-item.size-mid, .video-item.size-max { grid-column: span 1; grid-row: span 1; } }
.video-item.sort-hide { opacity: 0; transform: scale(0.95); pointer-events: none; }
.video-thumbnail { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 12px; transition: transform 0.3s ease, box-shadow 0.3s ease; }
.size-mid .video-thumbnail, .size-max .video-thumbnail { aspect-ratio: auto; height: auto; min-height: 200px; }
.video-link:hover .video-thumbnail { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
.video-title { margin-top: 10px; font-size: 1rem; font-weight: 600; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 0px !important; font-family: 'Noto Sans JP', sans-serif !important; }
.video-artist { font-size: 0.75rem; font-weight: 700; margin: 4px 0 2px 0; opacity: 0.8; font-family: 'Montserrat', sans-serif; }
.video-date { font-size: 0.7rem; opacity: 0.5; margin: 4px 0; }
.tag-container { margin-top: 4px; display: flex; flex-wrap: wrap; gap: 5px; }
.work-tag { font-size: 0.57rem; padding: 1px 6px; border-radius: 4px; border: 0.5px solid var(--text-color); opacity: 0.88; font-family: 'Montserrat', sans-serif; text-transform: uppercase; }
.wrapper { max-width: 1100px !important; padding-right: 40px !important; padding-left: 40px !important; }
.site-header .wrapper { max-width: 1100px !important; }
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');
:root { --bg-color: #ffffff; --text-color: #111111; }
html.dark-mode, body.dark-mode { --bg-color: #000000; --text-color: #eeeeee; background-color: #000000 !important; }
body { background-color: var(--bg-color) !important; color: var(--text-color) !important; transition: none !important; font-family: 'Noto Sans JP', sans-serif !important; font-weight: 700 !important; }
body.mode-transition { transition: background-color 0.5s ease, color 0.5s ease !important; }
.site-header { background-color: transparent !important; border: none !important; }
h1, h2, h3, .site-title { font-family: 'Montserrat', sans-serif !important; font-size: 1.4rem !important; font-weight: 700 !important; letter-spacing: -0.05em !important; color: var(--text-color) !important; }
.page-link { font-family: 'Montserrat', sans-serif !important; color: var(--text-color) !important; font-weight: 700 !important; text-transform: uppercase; font-size: 0.9rem !important; margin-left: 20px !important; text-decoration: none !important; }
.video-item h3 { font-family: 'Noto Sans JP', sans-serif !important; font-size: 0.85rem !important; height: auto !important; min-height: 1.3em; overflow: hidden; margin-bottom: 0px !important; line-height: 1.3; }
.rss-subscribe, .feed-icon, .site-footer { display: none !important; }
#mode-toggle { cursor: pointer; background: transparent; border: 1px solid var(--text-color); color: var(--text-color); padding: 6px 16px; border-radius: 20px; font-size: 0.75rem; position: fixed; top: 15px; right: 20px; z-index: 9999; font-weight: 700; font-family: 'Montserrat', sans-serif !important; transition: all 0.3s ease; backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
@media screen and (max-width: 1500px) { #mode-toggle { top: auto !important; bottom: 20px !important; right: 20px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.15); } }
#iris-in { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 0 500vmax var(--bg-color); z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 1.2s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-opening #iris-in { transform: translate(-50%, -50%) scale(500); }
#iris-out { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; background: var(--bg-color); z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 0.8s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-exiting #iris-out { transform: translate(-50%, -50%) scale(1.2) !important; }
body > *:not([id^="iris-"]) { opacity: 0; transition: opacity 0.8s ease-out; }
body.is-opening > *:not([id^="iris-"]) { opacity: 1; transition-delay: 0.2s; }
</style>
<button id="mode-toggle">🌙 Dark Mode</button>
<script>
function handleImageError(img) {
  const vId = img.dataset.videoId; if (!vId) return;
  const attempt = parseInt(img.dataset.errorAttempt || "0");
  const urls = [`https://i.ytimg.com/vi/${vId}/hqdefault.jpg`,`https://i.ytimg.com/vi/${vId}/mqdefault.jpg`,`https://i.ytimg.com/vi/${vId}/default.jpg`];
  if (attempt < urls.length) { img.dataset.errorAttempt = attempt + 1; img.src = urls[attempt]; }
}
document.addEventListener('DOMContentLoaded', () => {
  const items = Array.from(document.querySelectorAll('.video-item'));
  const artistFilter = document.getElementById('artist-filter');
  const tagFilter = document.getElementById('tag-filter');
  let activeArtist = 'ALL';
  let activeTags = new Set();

  const artists = new Set(['ALL']);
  const tags = new Set();
  items.forEach(item => {
    if (item.dataset.artist) artists.add(item.dataset.artist);
    item.dataset.tags.split(',').filter(t => t).forEach(t => tags.add(t));
  });

  function createBtn(text, container, onClick, isAll=false) {
    const btn = document.createElement('button');
    btn.className = 'filter-btn' + (isAll ? ' active' : '');
    btn.textContent = text;
    btn.onclick = () => onClick(btn, text);
    container.appendChild(btn);
  }

  if (artistFilter) {
    Array.from(artists).sort().forEach(a => createBtn(a, artistFilter, (btn, val) => {
      artistFilter.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active'); activeArtist = val; apply();
    }, a === 'ALL'));
  }

  Array.from(tags).sort().forEach(t => createBtn(t, tagFilter, (btn, val) => {
    btn.classList.toggle('active');
    if (activeTags.has(val)) activeTags.delete(val); else activeTags.add(val);
    apply();
  }));

  function apply() {
    items.forEach(item => {
      const aMatch = activeArtist === 'ALL' || item.dataset.artist === activeArtist;
      const tMatch = activeTags.size === 0 || Array.from(activeTags).every(t => item.dataset.tags.split(',').includes(t));
      if (aMatch && tMatch) {
        item.classList.remove('sort-hide'); item.style.display = ''; item.style.position = 'relative';
      } else {
        item.classList.add('sort-hide'); setTimeout(() => { if (item.classList.contains('sort-hide')) { item.style.display = 'none'; item.style.position = 'absolute'; } }, 400);
      }
    });
  }
});
const btn = document.getElementById('mode-toggle');
const body = document.body;
const html = document.documentElement;
if (localStorage.getItem('theme') === 'dark') { html.classList.add('dark-mode'); body.classList.add('dark-mode'); btn.textContent = '☀️ Light Mode'; }
btn.onclick = () => {
  body.classList.add('mode-transition');
  const isDark = html.classList.toggle('dark-mode');
  body.classList.toggle('dark-mode');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
  setTimeout(() => { body.classList.remove('mode-transition'); }, 500);
};
window.addEventListener('pageshow', () => { document.body.classList.add('is-opening'); });
document.querySelectorAll('a').forEach(link => {
  link.onclick = (e) => {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || link.target === "_blank") return;
    e.preventDefault(); document.body.classList.add('is-exiting');
    setTimeout(() => { window.location.href = href; }, 800);
  };
});
</script>
