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

  /* 3. 余計なものを消す */
  .rss-subscribe, .feed-icon { display: none !important; }
  body { -webkit-font-smoothing: antialiased; }

  /* メニュー全体の見た目を整える */
  .site-nav {
    background-color: transparent !important; /* 背景を透かしてスッキリ */
  }

  /* メニューの文字を細く、間隔を調整 */
  .page-link {
    color: #eee !important;
    font-weight: 400 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase; /* 文字を大文字にしてプロっぽく */
    font-size: 0.9rem !important;
    margin-left: 20px !important;
    text-decoration: none !important; /* 下線を消す */
    transition: 0.3s; /* ホバーした時の動きを滑らかに */
  }

  /* マウスを乗せた時だけ少し明るくする */
  .page-link:hover {
    color: #1e90ff !important;
    opacity: 0.8;
  }

  /* 左上のタイトル「Kakuly」をもっとデカく、強く */
  .site-title {
    font-size: 1.4rem !important;
    letter-spacing: -0.05em !important;
  }
</style>
