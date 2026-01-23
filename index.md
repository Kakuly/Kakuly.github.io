---
layout: home
title: Home
---
<div class="custom-section">
  <div class="section-content">

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


2006年生まれ。2020年から音楽活動を開始。
エレクトロポップ／ハイパーポップを中心に、たくさん迷いながら音楽を作っている。
元気に生きるために音楽を摂取します。いつもありがとう。
  </div>
</div>

<br>
<br>
<h2>CONTACT</h2><br>
<span><a href="https://x.com/kakuly_" target="_blank">DM on X</a></span><br>
kakuly.work@gmail.com<br>



  </div>
</div>

<style>
.custom-section {
    width: 100vw;
    margin-left: calc(-50vw + 50%); /* 画面幅いっぱいに広げる魔法のコード */
    background-size: cover;
    background-position: center;
    background-attachment: fixed; /* パララックス（視差効果）にしたい場合 */
    padding: 100px 0;
    color: white; /* 背景が暗い場合は文字を白に */
}
.section-content {
    max-width: 800px; /* コンテンツの幅を制限 */
    margin: 0 auto;
    padding: 0 20px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5); /* 文字を読みやすくする */
}
</style>


<hr style="width: 50%; margin: 40px auto; border-top: 1px solid var(--text-color); opacity: 0.3;">








<div id="iris-in"></div>
<div id="iris-out"></div>

<style>
.custom-section {
    width: 100vw;
    margin-left: calc(-50vw + 50%); /* 画面幅いっぱいに広げる魔法のコード */
    background-size: cover;
    background-position: center;
    background-attachment: fixed; /* パララックス（視差効果）にしたい場合 */
    padding: 100px 0;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important; /* iPhoneなどのブラウザ対策 */
    text-decoration-color: #ffffff !important; /* リンクの下線も白に */
}
  .custom-section a:hover {
    opacity: 0.7 !important;
}
.section-content {
    max-width: 800px; /* コンテンツの幅を制限 */
    margin: 0 auto;
    padding: 0 20px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5); /* 文字を読みやすくする */
}
</style>

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
    -webkit-font-smoothing: antialiased;
    letter-spacing: -0.05em !important;
    color: var(--text-color) !important;

  }

  .page-link {
    font-family: 'Montserrat', sans-serif !important;
    color: var(--text-color) !important;
    font-weight: 700 !important;
    -webkit-font-smoothing: antialiased;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
    font-size: 0.9rem !important;
    margin-left: 20px !important;
    text-decoration: none !important;
    transition: 0.3s;

  }

  .custom-section {
    width: 100vw;
    margin-left: calc(-50vw + 50%);
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    padding: 100px 0;
    
    /* ↓ ここがポイント：画像の上に黒いグラデーションを重ねる */
    background-image: 
        linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.7)), 
        url('/assets/img/header_kakuly.jpg');
    
    color: #ffffff !important; /* 文字を白に固定 */
    }

.section-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
    /* 文字に深みを出す影 */
    text-shadow: 0 4px 15px rgba(0,0,0,0.8);
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
    /* border: 0.1px solid var(--text-color); */
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
    filter: invert(1) grayscale(100%) brightness(1.5);
    opacity: 0.7;
    transition: 0.3s;
  }

  /* html.dark-mode .sns-links img { filter: invert(1) grayscale(100%) brightness(1.5); } */

  /* 7. 不要な要素の削除（Worksと同じ） */
  .rss-subscribe, .feed-icon, .site-footer { display: none !important; }

/* --- モード切替ボタンの設定（レスポンシブ対応） --- */
#mode-toggle { 
    cursor: pointer; 
    background: transparent; 
    border: 1px solid var(--text-color); 
    color: var(--text-color); 
    padding: 6px 16px; 
    border-radius: 20px; 
    font-size: 0.75rem; 
    position: fixed; 
    top: 15px; 
    right: 20px; 
    z-index: 9999; 
    font-weight: 700;
    font-family: 'Montserrat', sans-serif !important; /* フォントを明示的に指定 */
    transition: all 0.3s ease;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

/* 画面幅が1300px以下になったら右下に移動 */
@media screen and (max-width: 1500px) {
    #mode-toggle {
        top: auto !important;
        bottom: 20px !important;
        right: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15); /* 下に移動したときに見やすく */
    }
}

  /* スマホ対応 */
  @media (max-width: 800px) {
    .profile-container { flex-direction: column; align-items: flex-start; }
    .profile-name { font-size: 5rem !important; }
    .profile-icon { width: 200px; height: 200px; }
  }




/* 1. 演出用の影を「全要素の頂点」に持っていく */
#iris-in {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  box-shadow: 0 0 0 500vmax var(--bg-color);
  /* z-indexを極端に大きくしてヘッダーを封じ込める */
  z-index: 9999999 !important; 
  pointer-events: none;
  transform: translate(-50%, -50%) scale(0);
  transition: transform 1.2s cubic-bezier(0.85, 0, 0.15, 1);
}

/* 2. ヘッダーを含むすべてのコンテンツを、最初は「完全に透明」にする */
body > *:not([id^="iris-"]) {
  opacity: 0 !important;
  transition: opacity 0.8s ease-out;
}

/* 3. 穴が開き始めたら、フワッと表示する */
body.is-opening > *:not([id^="iris-"]) {
  opacity: 1 !important;
}

/* 4. ヘッダーが突き抜けないように念のためz-indexを下げる */
.site-header {
  z-index: 100 !important;
}

/* 実行時：穴を全開にする */
body.is-opening #iris-in {
  /* visibility: visible; ← これも不要 */
  transform: translate(-50%, -50%) scale(500);
}

/* --- アウト（退場）：板が広がる演出 --- */
#iris-out {
  position: fixed;
  top: 50%; left: 50%;
  width: 150vmax; height: 150vmax;
  background-color: var(--bg-color);
  border-radius: 50%;
  z-index: 100001;
  pointer-events: none;
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.8s cubic-bezier(0.85, 0, 0.15, 1);
}

body.is-exiting #iris-out {
  transform: translate(-50%, -50%) scale(1.2) !important;
}

/* =========================================
   ★追加：コンテンツの中身をフェードインさせる設定
   ========================================= */
/* 演出用パーツ(#iris-...)以外の、body直下のすべての要素を対象にする */
body > *:not([id^="iris-"]) {
  opacity: 0; /* 最初は透明にして隠す */
  transition: opacity 0.8s ease-out; /* フワッと表示させる */
}

/* アイリスが開くと同時に、中身も不透明（見える状態）にする */
body.is-opening > *:not([id^="iris-"]) {
  opacity: 1;
  transition-delay: 0.2s; /* アイリスが少し開いてから表示開始する時差演出 */
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




function startIris() {
  document.body.classList.remove('is-opening', 'is-exiting');
  // ブラウザの描画を待つために少し遅らせる
  requestAnimationFrame(() => {
    setTimeout(() => {
      document.body.classList.add('is-opening');
    }, 50);
  });
}

// ページ表示時に必ず実行
window.addEventListener('pageshow', startIris);

// リンククリック時
document.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', (e) => {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.includes('mailto:') || link.target === "_blank") return;
    
    e.preventDefault();
    document.body.classList.add('is-exiting');
    setTimeout(() => { window.location.href = href; }, 800);
  });
});
</script>

<!-- NEWS_START -->

<div class="news-section-wrapper">
  <h2 class="section-title">NEWS</h2>
  <div class="news-container-outer">
    <button class="news-nav-btn prev" onclick="scrollNews(-1)" id="news-prev-btn">&#10094;</button>
    <div class="news-scroll-container" id="news-scroll-container">
      <div class="news-card" onclick="openNewsModal('2')">
        <div class="news-card-date">2026-01-25</div>
        <div class="news-card-title">新しい楽曲を公開しました</div>
        <div class="news-card-content-hidden" id="news-content-2" style="display:none;">YouTubeにて新しい制作楽曲を公開しました。ぜひWorksページからチェックしてください。</div>
      </div>
      <div class="news-card" onclick="openNewsModal('1')">
        <div class="news-card-date">2026-01-23</div>
        <div class="news-card-title">ポートフォリオサイトをリニューアルしました</div>
        <div class="news-card-content-hidden" id="news-content-1" style="display:none;">ポートフォリオサイトのデザインを一新し、ニュースセクションを追加しました。今後はこちらで最新情報をお届けします。</div>
      </div>
      <div class="news-card" onclick="openNewsModal('news_1769141876861')">
        <div class="news-card-date">2026-01-23</div>
        <div class="news-card-title">pixiv fanboxにて有料記事を公開しました</div>
        <div class="news-card-content-hidden" id="news-content-news_1769141876861" style="display:none;">先日公開した、snowflakingについて公開しました<br>https://kakuly.fanbox.cc/</div>
      </div>
      <div class="news-card" onclick="openNewsModal('news_1769141879300')">
        <div class="news-card-date">2026-01-20</div>
        <div class="news-card-title">sd</div>
        <div class="news-card-content-hidden" id="news-content-news_1769141879300" style="display:none;">dsdsdsd</div>
      </div>
      <div class="news-card" onclick="openNewsModal('news_1769141880522')">
        <div class="news-card-date">2026-01-10</div>
        <div class="news-card-title">asdads</div>
        <div class="news-card-content-hidden" id="news-content-news_1769141880522" style="display:none;">asdasd</div>
      </div>
      <div class="news-card" onclick="openNewsModal('news_1769141886557')">
        <div class="news-card-date">2025-12-08</div>
        <div class="news-card-title">sfdhs</div>
        <div class="news-card-content-hidden" id="news-content-news_1769141886557" style="display:none;">fhsdfhsdfh</div>
      </div>
      <div class="news-card" onclick="openNewsModal('news_1769141891071')">
        <div class="news-card-date">2025-07-25</div>
        <div class="news-card-title">sfdhsdf</div>
        <div class="news-card-content-hidden" id="news-content-news_1769141891071" style="display:none;">hsdfh</div>
      </div>
    </div>
    <button class="news-nav-btn next" onclick="scrollNews(1)" id="news-next-btn">&#10095;</button>
  </div>
</div>

<div id="news-modal" class="modal">
  <div class="modal-content">
    <span class="close-modal" onclick="closeNewsModal()">&times;</span>
    <div id="modal-date" class="modal-date"></div>
    <h2 id="modal-title" class="modal-title"></h2>
    <div id="modal-body" class="modal-body"></div>
  </div>
</div>

<style>
.news-section-wrapper { margin: 40px 0; position: relative; z-index: 10; }
.news-section-wrapper .section-title { font-family: 'Montserrat', sans-serif; font-size: 1.8rem; margin-bottom: 20px; letter-spacing: -0.05em; }
.news-container-outer { position: relative; display: flex; align-items: center; }
.news-scroll-container { 
  display: flex; 
  overflow-x: auto; 
  gap: 20px; 
  padding: 20px 5px;
  scrollbar-width: none;
  -ms-overflow-style: none;
  scroll-behavior: smooth;
  width: 100%;
}
.news-scroll-container::-webkit-scrollbar { display: none; }

.news-card { 
  flex: 0 0 280px; 
  background: var(--bg-color); 
  border: 1px solid var(--text-color); 
  border-radius: 15px; 
  padding: 20px; 
  cursor: pointer; 
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  color: var(--text-color);
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.news-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
.news-card-date { font-family: 'Montserrat', sans-serif; font-size: 0.75rem; opacity: 0.7; margin-bottom: 8px; }
.news-card-title { font-size: 1rem; font-weight: 700; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }

.news-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: var(--bg-color);
  color: var(--text-color);
  border: 1px solid var(--text-color);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 11;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  opacity: 0;
  pointer-events: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.news-container-outer:hover .news-nav-btn.visible { opacity: 1; pointer-events: auto; }
.news-nav-btn.prev { left: -20px; }
.news-nav-btn.next { right: -20px; }
.news-nav-btn:hover { background: var(--text-color); color: var(--bg-color); }

.modal { display: none; position: fixed; z-index: 100001; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.8); backdrop-filter: blur(10px); }
.modal-content { background-color: var(--bg-color); margin: 10% auto; padding: 40px; border-radius: 20px; width: 85%; max-width: 600px; position: relative; color: var(--text-color); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
.close-modal { color: var(--text-color); float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
.modal-date { font-family: 'Montserrat', sans-serif; font-size: 0.9rem; opacity: 0.5; margin-bottom: 10px; }
.modal-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 20px; line-height: 1.3; }
.modal-body { font-size: 1rem; line-height: 1.8; }
</style>

<script>
function scrollNews(direction) {
  const container = document.getElementById('news-scroll-container');
  const scrollAmount = 600 * direction;
  container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
}

function updateNewsNav() {
  const container = document.getElementById('news-scroll-container');
  const prevBtn = document.getElementById('news-prev-btn');
  const nextBtn = document.getElementById('news-next-btn');
  if (!container || !prevBtn || !nextBtn) return;
  
  const isScrollable = container.scrollWidth > container.clientWidth;
  if (isScrollable) {
    prevBtn.classList.toggle('visible', container.scrollLeft > 10);
    nextBtn.classList.toggle('visible', container.scrollLeft < (container.scrollWidth - container.clientWidth - 10));
  } else {
    prevBtn.classList.remove('visible');
    nextBtn.classList.remove('visible');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('news-scroll-container');
  if (container) {
    container.addEventListener('scroll', updateNewsNav);
    window.addEventListener('resize', updateNewsNav);
    setTimeout(updateNewsNav, 500);
  }
});

function openNewsModal(id) {
  const contentElement = document.getElementById(`news-content-${id}`);
  const card = contentElement.closest('.news-card');
  const title = card.querySelector('.news-card-title').innerText;
  const date = card.querySelector('.news-card-date').innerText;
  const content = contentElement.innerHTML;
  document.getElementById('modal-title').innerText = title;
  document.getElementById('modal-date').innerText = date;
  document.getElementById('modal-body').innerHTML = content;
  document.getElementById('news-modal').style.display = "block";
  document.body.style.overflow = "hidden";
}
function closeNewsModal() {
  document.getElementById('news-modal').style.display = "none";
  document.body.style.overflow = "auto";
}
window.onclick = function(event) {
  if (event.target == document.getElementById('news-modal')) closeNewsModal();
}
</script>

<!-- NEWS_END -->
