---
layout: page
title: Works
permalink: /works/
---

## YouTube Playlist (Auto Updated)

<div class="video-grid">

<div class="video-item">
  <h3>枕元 / kafu</h3>
  <iframe src="https://www.youtube.com/embed/x0VqpfLdEVI" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - direct & loop [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/YDPnby_OWWg" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - freedom (remix) [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/uuFFToqXXsQ" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - connect [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/oj7AKQW6PDY" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - glory days (feat.Akari24) [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/HDFmhVzat6Y" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - hold the loop [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/UJbm_K-6YlU" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - cut and try [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/OhvvTOyJl78" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - about XX (feat.kafu) [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/wfc1V8YeuBQ" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - 脳dead U (feat.nui) [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/RjsNyzywWtk" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - 三角 [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/Wg0t0XrodUI" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - (don't know) you [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/s8wtr1bBHMU" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly × tato - [voicememo] [official audio]</h3>
  <iframe src="https://www.youtube.com/embed/nwemY-pMKQ0" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Digital Album "DIRECT & LOOP" [XFD]</h3>
  <iframe src="https://www.youtube.com/embed/nJwjaBef_jI" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>[VocaDuo2025] いちご納豆ごはん - garden</h3>
  <iframe src="https://www.youtube.com/embed/BWAdNu7HnJE" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>[VocaDuo2025] Quilter - dots</h3>
  <iframe src="https://www.youtube.com/embed/wlmevRPxajk" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Wa!ter×Kakuly - はか</h3>
  <iframe src="https://www.youtube.com/embed/rQ3cbuAqb3o" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Peterparker69, 野田洋次郎 - Hey phone (Kakuly remix + tato cover)</h3>
  <iframe src="https://www.youtube.com/embed/lG2I7mA0VGE" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Kakuly - re:create (feat.重音テトSV)</h3>
  <iframe src="https://www.youtube.com/embed/3uh6S-RRqAM" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>Akari24 - Juvenile Delinquency (Kakuly ver.)</h3>
  <iframe src="https://www.youtube.com/embed/U9XdrefRvCg" frameborder="0" allowfullscreen></iframe>
</div>

<div class="video-item">
  <h3>hello / hatsune miku</h3>
  <iframe src="https://www.youtube.com/embed/paIePEOWhLc" frameborder="0" allowfullscreen></iframe>
</div>

</div>


<style>
  /* --- ベースの設定 --- */
  :root {
    --bg-color: #ffffff;
    --text-color: #111111;
    --header-bg: #ffffff;
  }
  
  /* --- ダークモード時の色定義 --- */
  body.dark-mode {
    --bg-color: #000000;
    --text-color: #eeeeee;
    --header-bg: #000000;
  }

  body { 
    background-color: var(--bg-color) !important; 
    color: var(--text-color) !important; 
    transition: 0.3s; /* 切り替えをふわっとさせる */
  }

  .site-header, .site-title, .page-link { 
    background-color: var(--header-bg) !important; 
    color: var(--text-color) !important; 
  }

  /* ギャラリーの設定（4列用） */
  .video-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)) !important;
    gap: 30px;
  }

  /* --- 切り替えボタンの見た目 --- */
  #mode-toggle {
    cursor: pointer;
    background: none;
    border: 1px solid var(--text-color);
    color: var(--text-color);
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
  }
</style>

<button id="mode-toggle">🌙 Dark Mode</button>

<script>
  const btn = document.getElementById('mode-toggle');
  const body = document.body;

  // ページ読み込み時に保存されたモードを適用
  if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-mode');
    btn.textContent = '☀️ Light Mode';
  }

  // クリックイベント
  btn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    
    if (body.classList.contains('dark-mode')) {
      localStorage.setItem('theme', 'dark');
      btn.textContent = '☀️ Light Mode';
    } else {
      localStorage.setItem('theme', 'light');
      btn.textContent = '🌙 Dark Mode';
    }
  });
</script>

  /* 2. フォントを「ダサくない」モダンなものに変える */
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');
  body, p, li { font-family: 'Noto Sans JP', sans-serif !important; line-height: 1.8; letter-spacing: -0.03em !important; }
  .site-title, h1, h2, h3 { font-family: 'Montserrat', sans-serif !important; font-weight: 700:  !important; letter-spacing: -0.03em !important; }
  
  /* タイル状に並べる設定（横4つ） */
  .video-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)) !important;
    gap: 40px 20px !important;
    padding-top: 20px;
  }
  
  .video-item h3 {
    font-size: 0.85rem !important;
    height: 3em;
    overflow: hidden;
    margin-bottom: 10px !important;
  }
  
  iframe {
    width: 100% !important;
    aspect-ratio: 16 / 9;
    border-radius: 8px;
    background: #111;
  }
</style>
