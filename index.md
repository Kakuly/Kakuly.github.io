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


<div id="page-transition-overlay"></div>

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

#page-transition-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: var(--bg-color); /* 画面を隠す幕の色 */
  z-index: 999999;
  pointer-events: none;
  /* ★ポイント：最初は穴がない（circle(0%)）状態で画面を真っさらな幕にする */
  clip-path: circle(0% at 50% 50%);
}

/* イン：幕を「0%（穴なし）」から「150%（穴全開）」へ広げる */
/* これで「幕がくり抜かれて中が見える」動きになります */
body.is-loading #page-transition-overlay {
  animation: iris-in 0.8s cubic-bezier(0.85, 0, 0.15, 1) forwards;
}

/* アウト：逆に「150%（全開）」から「0%（穴なし）」へ閉じる */
/* これで「幕の穴が閉じて画面が塗りつぶされる」動きになります */
body.is-exiting #page-transition-overlay {
  animation: iris-out 0.8s cubic-bezier(0.85, 0, 0.15, 1) forwards;
}

@keyframes iris-in {
  /* 0% (幕が全面にある) -> 150% (穴が広がって消える) */
  from { clip-path: circle(0% at 50% 50%); }
  to { clip-path: circle(150% at 50% 50%); }
}

@keyframes iris-out {
  /* 150% (穴が開いている) -> 0% (穴が閉じて幕になる) */
  from { clip-path: circle(150% at 50% 50%); }
  to { clip-path: circle(0% at 50% 50%); }
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


// 1. ページ読み込み開始時にクラスを付与
document.body.classList.add('is-loading');

window.addEventListener('load', () => {
  // 2. リンククリックで「退場」アニメ開始
  document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('#') || href.includes('mailto:') || link.target === "_blank") return;
      
      e.preventDefault();
      document.body.classList.remove('is-loading'); // loadingを外して
      document.body.classList.add('is-exiting');    // exitingをつける

      setTimeout(() => {
        window.location.href = href;
      }, 800);
    });
  });
});
  
</script>
