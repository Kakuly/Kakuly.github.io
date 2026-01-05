---
layout: home
title: Home
---
<div class="profile-container">
  <img src="/assets/img/profile.png" class="profile-icon">
  
  <div class="profile-text">
    <p class="profile-name">Kakuly</p>
    
    <div class="sns-links">
      <a href="https://soundcloud.com/kakuly-uni" target="_blank" rel="noopener">
        <img src="https://upload.wikimedia.org/wikipedia/commons/a/a2/Antu_soundcloud.svg" alt="SoundCloud">
      </a>
      <a href="https://x.com/kakuly_" target="_blank" rel="noopener">
        <img src="https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg" alt="X">
      </a>
    </div>
  </div>
</div>

2006年生まれ。2020年から音楽活動を開始。
エレクトロポップ／ハイパーポップを中心に、たくさん迷いながら音楽を作っている。
元気に生きるために音楽を摂取します。いつもありがとう。

<style>
  /* 1. サイト全体の最大幅（Worksと同じ位置） */
  .wrapper {
    max-width: 1100px !important;
    padding-right: 40px !important;
    padding-left: 40px !important;
  }
  .site-header .wrapper {
    max-width: 1100px !important;
  }

  /* 2. フォント読み込み（Worksと同じ） */
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');

  /* 3. カラー変数とダークモード（Worksと同じ位置に配置） */
  :root {
    --bg-color: #ffffff;
    --text-color: #111111;
    --link-color: #0066cc;
  }
  
  html.dark-mode, body.dark-mode {
    --bg-color: #000000;
    --text-color: #eeeeee;
    --link-color: #80c0ff;
    background-color: #000000 !important;
  }

  /* 4. 全体レイアウト（bodyの設定を先に読ませる） */
  body { 
    background-color: var(--bg-color) !important; 
    color: var(--text-color) !important; 
    transition: none !important; 
    font-family: 'Noto Sans JP', sans-serif !important;
    font-weight: 700 !important;
    -webkit-font-smoothing: antialiased;
  }

  body.mode-transition {
    transition: background-color 0.5s ease, color 0.5s ease !important;
  }

  /* 5. ヘッダー・ナビゲーション（Worksのセクション4と完全同期） */
  .site-header { background-color: transparent !important; border: none !important; -webkit-font-smoothing: antialiased; }
  
  h1, h2, h3, .site-title, .profile-name { 
    font-family: 'Montserrat', sans-serif !important;
    font-size: 1.4rem !important; 
    font-weight: 700 !important;
    letter-spacing: -0.05em !important;
    color: var(--text-color) !important;
    -webkit-font-smoothing: antialiased;
  }

  .page-link {
    font-family: 'Montserrat', sans-serif !important;
    color: var(--text-color) !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
    font-size: 0.9rem !important;
    margin-left: 20px !important;
    text-decoration: none !important;
    transition: 0.3s;
    -webkit-font-smoothing: antialiased;
  }

  /* 6. 個別要素（Home専用の設定だが、強さをWorksに合わせる） */
  .profile-name {
    font-size: 8.5rem !important; /* フォントや太さは上でh3等と同期済み */
    line-height: 1;
  }

  .profile-container {
    display: flex;
    align-items: center;
    gap: 40px;
    margin-bottom: 30px;
  }

  .profile-icon {
    width: 300px;
    height: 300px;
    border-radius: 7%;
    object-fit: cover;
    border: 0.1px solid var(--text-color);
    flex-shrink: 0;
  }

  .sns-links {
    display: flex;
    gap: 45px !important;
    margin-top: 15px;
  }

  .sns-links img {
    width: 35px;
    height: 35px;
    filter: grayscale(100%) brightness(1.2);
    opacity: 0.7;
    transition: 0.3s;
  }

  html.dark-mode .sns-links img { filter: invert(1) grayscale(100%) brightness(1.5); }

  /* 7. 不要な要素の削除（Worksと同じ） */
  .rss-subscribe, .feed-icon, .site-footer { display: none !important; }

  /* 8. モード切り替えボタン（Worksと同じ） */
  #mode-toggle {
    cursor: pointer;
    background: none;
    border: 1px solid var(--text-color);
    color: var(--text-color);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    position: fixed;
    top: 15px;
    right: 20px;
    z-index: 9999;
    font-weight: bold;
    font-family: 'Montserrat', sans-serif !important;
  }

  /* スマホ対応 */
  @media (max-width: 800px) {
    .profile-container { flex-direction: column; align-items: flex-start; }
    .profile-name { font-size: 5rem !important; }
    .profile-icon { width: 200px; height: 200px; }
  }

/* --- イン（入場）の設定：body自体の切り抜き --- */
body {
  background-color: var(--bg-color) !important;
  /* 最初は穴が 0% */
  clip-path: circle(0% at 50% 50%);
  transition: clip-path 0.8s cubic-bezier(0.85, 0, 0.15, 1);
}

/* 読み込み完了後、穴を広げて中身を見せる */
body:not(.is-loading) {
  clip-path: circle(150% at 50% 50%);
}

/* --- アウト（退場）の設定：丸い板を広げる --- */
body::before {
  content: "";
  position: fixed;
  top: 50%; left: 50%;
  width: 150vmax; height: 150vmax;
  background-color: var(--bg-color); 
  z-index: 99999;
  pointer-events: none;
  border-radius: 50%;
  /* 最初は 0（隠しておく） */
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.8s cubic-bezier(0.85, 0, 0.15, 1);
}

/* リンクを押した時、板を 1.5倍 まで広げて中身を隠す */
body.is-exiting::before {
  transform: translate(-50%, -50%) scale(1.5) !important;
}
  
  </style>

<script>
  (function() {
    if (localStorage.getItem('theme') === 'dark') {
      document.documentElement.classList.add('dark-mode');
    }
  })();
</script>

<button id="mode-toggle">🌙 Dark Mode</button>

<script>
  const btn = document.getElementById('mode-toggle');
  const body = document.body;
  const html = document.documentElement;

  if (localStorage.getItem('theme') === 'dark') {
    html.classList.add('dark-mode');
    body.classList.add('dark-mode');
    btn.textContent = '☀️ Light Mode';
  }

  btn.addEventListener('click', () => {
    body.classList.add('mode-transition');
    const isDark = html.classList.toggle('dark-mode');
    body.classList.toggle('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
    setTimeout(() => {
      body.classList.remove('mode-transition');
    }, 500);
  });


window.addEventListener('load', () => {
  // イン：0.1秒後に body の穴を開ける
  setTimeout(() => {
    document.body.classList.remove('is-loading');
  }, 100);

  // アウト：クリックで body::before の板を広げる
  document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      // 外部リンクや特殊リンクは除外
      if (!href || href.startsWith('#') || href.includes('mailto:') || link.target === "_blank") return;
      
      e.preventDefault();
      document.body.classList.add('is-exiting');

      // 板が広がる時間を待ってから移動
      setTimeout(() => {
        window.location.href = href;
      }, 800);
    });
  });
});
  
</script>
