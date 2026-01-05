---
layout: home
title: Home
---
![プロフィール](/assets/img/profile.png)
2006年生まれ。2020年から音楽活動を開始。
エレクトロポップ／ハイパーポップを中心に、たくさん迷いながら音楽を作っている。
元気に生きるために音楽を摂取します。いつもありがとう。

- [SoundCloud](https://soundcloud.com/kakuly-uni)
- [Twitter / X](https://x.com/kakuly_)

<style>
  <img src="/assets/img/profile.png" width="75" alt="プロフィール">
  /* 1. フォント読み込み */
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');

  /* 2. カラー変数（Lightがデフォルト） */
  :root {
    --bg-color: #ffffff;
    --text-color: #111111;
    --link-color: #0066cc;
  }
  
  /* ダークモード時の上書き */
  html.dark-mode, body.dark-mode {
    --bg-color: #000000;
    --text-color: #eeeeee;
    --link-color: #80c0ff;
    background-color: #000000 !important; /* HTMLごと黒くする */
  }

  /* 3. 全体レイアウト */
body { 
  background-color: var(--bg-color) !important; 
  color: var(--text-color) !important; 
  /* 通常時は transition をオフにしてパカつきをゼロにする */
  transition: none !important; 
  font-family: 'Noto Sans JP', sans-serif !important;
  font-weight: 700 !important;
  -webkit-font-smoothing: antialiased;
}

/* ボタンを押した時だけ付与するクラス */
body.mode-transition {
  transition: background-color 0.5s ease, color 0.5s ease !important;
}

  /* 4. 見出し・タイトルのフォント統一 */
  h1, h2, h3, .site-title, .page-link, #mode-toggle { 
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-color) !important;
  }

  .site-header { background-color: transparent !important; border: none !important; }
  .site-title { font-size: 1.4rem !important; letter-spacing: -0.05em !important; }
  .page-link { font-size: 0.9rem !important; margin-left: 20px !important; text-transform: uppercase; text-decoration: none !important; }
  a { color: var(--link-color); }
  .rss-subscribe, .feed-icon { display: none !important; }

  /* 5. モード切り替えボタン */
  #mode-toggle {
    cursor: pointer;
    background: none;
    border: 1px solid var(--text-color);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    position: fixed;
    top: 15px;
    right: 20px;
    z-index: 9999;
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

  // 初期化スクリプトはそのまま（白飛び防止用）
  if (localStorage.getItem('theme') === 'dark') {
    html.classList.add('dark-mode');
    body.classList.add('dark-mode');
    btn.textContent = '☀️ Light Mode';
  }

  btn.addEventListener('click', () => {
    // 1. transition用のクラスを付与
    body.classList.add('mode-transition');

    // 2. モードを切り替え
    const isDark = html.classList.toggle('dark-mode');
    body.classList.toggle('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';

    // 3. アニメーションが終わる頃にクラスを外す（次のページ移動に備える）
    setTimeout(() => {
      body.classList.remove('mode-transition');
    }, 500); // 0.4sのアニメーションより少し長く設定
  });
</script>

