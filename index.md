---
layout: home
title: Home
---
2006年生まれ。2020年から音楽活動を開始。
エレクトロポップ／ハイパーポップを中心に、たくさん迷いながら音楽を作っている。
元気に生きるために音楽を摂取します。いつもありがとう。

- [SoundCloud](https://soundcloud.com/kakuly-uni)
- [Twitter / X](https://x.com/kakuly_)

<style>
  /* 1. フォント読み込み */
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');

  /* 2. カラー変数設定 */
  :root {
    --bg-color: #ffffff;
    --text-color: #111111;
    --link-color: #0066cc; /* ライトモード時のリンク色 */
  }
  
  body.dark-mode {
    --bg-color: #000000;
    --text-color: #eeeeee;
    --link-color: #80c0ff; /* ダークモード時のリンク色 */
  }

  /* 3. 全体レイアウト */
  body { 
    background-color: var(--bg-color) !important; 
    color: var(--text-color) !important; 
    transition: 0.3s;
    font-family: 'Noto Sans JP', sans-serif !important;
    line-height: 1.8;
    -webkit-font-smoothing: antialiased;
  }

  /* 4. ヘッダー・ナビゲーション（フォント同期） */
  .site-header { background-color: transparent !important; border: none !important; }
  
  h1, h2, h3, .site-title { 
    font-family: 'Montserrat', sans-serif !important;
    font-size: 1.4rem !important; 
    font-weight: 700 !important;
    letter-spacing: -0.05em !important;
    color: var(--text-color) !important;
  }

  .page-link {
    font-family: 'Montserrat', sans-serif !important;
    color: var(--text-color) !important; /* モードに合わせて色を変える */
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
    font-size: 0.9rem !important;
    margin-left: 20px !important;
    text-decoration: none !important;
    transition: 0.3s;
  }

  .page-link:hover {
    opacity: 0.6;
  }

  /* 5. コンテンツ内のリンク色 */
  a { color: var(--link-color); }

  /* 6. 不要な要素の削除 */
  .rss-subscribe, .feed-icon { display: none !important; }

  /* 7. モード切り替えボタン */
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
</style>
<button id="mode-toggle">🌙 Dark Mode</button>

<script>
  const btn = document.getElementById('mode-toggle');
  const body = document.body;

  if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-mode');
    btn.textContent = '☀️ Light Mode';
  }

  btn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const isDark = body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
  });
</script>
"""
