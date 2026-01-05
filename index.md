---
layout: home
title: Home
---
<div class="profile-container">
  <img src="/assets/img/profile.png" class="profile-icon">
  
  <div class="profile-text">
    <p class="profile-name">Kakuly</p>
  </div>
</div>

<style>
  /* 横並びのレイアウト設定 */
  .profile-container {
    display: flex;
    align-items: center;  /* 上下中央揃え */
    gap: 30px;            /* 画像と文字の間の距離 */
    margin-bottom: 20px;
  }

  /* 画像の設定（これまでの設定を維持） */
  .profile-icon {
    width: 300px;
    height: 300px;
    border-radius: 7%;
    object-fit: cover;
    border: 0.1px solid var(--text-color);
    flex-shrink: 0;       /* 画面が狭くなっても画像が潰れないように固定 */
  }

  /* 名前の設定 */
  .profile-name {
    font-size: 8.5rem;
    font-weight: bold;
    margin: 0;            /* 余計な隙間を消して中央に揃えやすくする */
    font-family: 'Montserrat', sans-serif !important;
  }

  /* スマホなど画面が狭い時の調整（任意） */
  @media (max-width: 600px) {
    .profile-container {
      flex-direction: column; /* 縦並びにする */
      align-items: flex-start;
      gap: 15px;
    }
    .profile-icon {
      width: 200px; /* スマホでは少し小さくする */
      height: 200px;
    }
  }
</style>

2006年生まれ。2020年から音楽活動を開始。
エレクトロポップ／ハイパーポップを中心に、たくさん迷いながら音楽を作っている。
元気に生きるために音楽を摂取します。いつもありがとう。

<div class="sns-links">
  <a href="https://soundcloud.com/kakuly-uni" target="_blank" rel="noopener">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a2/Antu_soundcloud.svg" alt="SoundCloud">
  </a>

  <a href="https://x.com/kakuly_" target="_blank" rel="noopener">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg" alt="X">
  </a>
</div>

<style>
  .sns-links {
  display: flex;
  /* ここを 20px から 45px くらいに増やす */
  gap: 45px !important; 
  
  margin-top: 25px; /* 上の名前との距離も少し広げるとゆったりします */
}
.sns-links img {
  width: 35px;
  height: 35px;
  object-fit: contain;
  transition: transform 0.2s, filter 0.3s, opacity 0.3s; /* 変化を滑らかに */
  
  /* 1. 全体をグレーにする */
  filter: grayscale(100%) brightness(1.2); 
  opacity: 0.7; /* 少し透かして背景に馴染ませる */
}

/* 2. マウスを乗せた時の演出（お好みで選んでね） */
.sns-links img:hover {
  transform: translateY(-3px);
  opacity: 1;

  /* パターンB：マウスを乗せてもモノクロのまま（さらに明るくするだけ） */
  filter: grayscale(100%) brightness(2); 
}

/* 3. ダークモードの時の微調整 */
html.dark-mode .sns-links img {
  /* 黒背景でも見えやすいように、白っぽく反転させてからグレーにする */
  filter: invert(1) grayscale(100%) brightness(1.5);
}
</style>

<style>
  /* サイト全体の最大幅を上書き */
.wrapper {
  max-width: 1100px !important; /* 800pxから1100pxに拡張 */
  padding-right: 40px !important;
  padding-left: 40px !important;
}

/* ヘッダーの幅も合わせる */
.site-header .wrapper {
  max-width: 1100px !important;
}

/* Worksの動画グリッドをより広々と見せる調整 */
.video-grid {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)) !important; /* 1つ1つの動画を少し大きく */
  gap: 30px !important;
}

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

  /* 全体レイアウト */
/* 1. 基本の太さを設定（本文に適用される） */
body { 
  background-color: var(--bg-color) !important; 
  color: var(--text-color) !important; 
  font-family: 'Noto Sans JP', sans-serif !important;
  font-weight: 700 !important; /* 本文はしっかり太め */
}

/* ボタンを押した時だけ付与するクラス */
body.mode-transition {
  transition: background-color 0.5s ease, color 0.5s ease !important;
}

  /* 4. 見出し・タイトルのフォント統一 */
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
    color: var(--text-color) !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
    font-size: 0.9rem !important;
    margin-left: 20px !important;
    text-decoration: none !important;
    transition: 0.3s;
  }

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

