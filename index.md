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
  /* 1. フォント読み込み（300, 400, 700をセット） */
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');

  /* 2. 全体レイアウト */
  .wrapper {
    max-width: 1100px !important;
    padding: 0 40px !important;
  }
  .site-header .wrapper { max-width: 1100px !important; }

  /* 3. ベース設定（本文） */
  body { 
    background-color: var(--bg-color) !important; 
    color: var(--text-color) !important; 
    font-family: 'Noto Sans JP', sans-serif !important;
    font-weight: 700 !important; /* 本文の太さは維持 */
    -webkit-font-smoothing: antialiased;
  }

  /* A. サイト全体の共通タイトルや名前（入力した通りの文字が出る） */
  .profile-name, h1, h2, h3, .site-title { 
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 700 !important;      /* 太字 */
    letter-spacing: -0.02em !important; /* 少し詰めて力強く */
    color: var(--text-color) !important;
    -webkit-font-smoothing: antialiased;
    margin: 0;
    /* text-transform: uppercase; ← これを消すことで小文字が通るようになります */
  }

  /* B. ページリンク（ここだけ強制的に大文字にする） */
  .page-link {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 700 !important;      /* 太字 */
    text-transform: uppercase;         /* ★ここだけ大文字にする */
    letter-spacing: 0.05em !important; /* Worksと同じ字間 */
    font-size: 0.9rem !important;
    margin-left: 20px !important;
    text-decoration: none !important;
    color: var(--text-color) !important;
    -webkit-font-smoothing: antialiased;
  }

  /* Kakuly の名前のサイズ設定 */
  .profile-name {
    font-size: 8.5rem;
    line-height: 1;
  }

  /* 5. プロフィール・SNSのレイアウト */
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

  .sns-links img:hover {
    transform: translateY(-3px);
    opacity: 1;
    filter: grayscale(100%) brightness(2);
  }

  /* ダークモード設定 */
  :root { --bg-color: #ffffff; --text-color: #111111; }
  html.dark-mode { --bg-color: #000000; --text-color: #eeeeee; }
  html.dark-mode .sns-links img { filter: invert(1) grayscale(100%) brightness(1.5); }

  /* スマホ対応 */
  @media (max-width: 800px) {
    .profile-container { flex-direction: column; align-items: flex-start; }
    .profile-name { font-size: 5rem; }
    .profile-icon { width: 200px; height: 200px; }
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
