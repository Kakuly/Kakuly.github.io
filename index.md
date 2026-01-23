---
layout: page
title: Home
---

<!-- ヘッダー画像とプロファイルオーバーレイのカスタムHTML/CSSを挿入 -->
<style>
/* ヘッダー画像とオーバーレイ */
.kakuly-hero-section {
  position: relative;
  width: 100vw;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  padding: 100px 0;
  margin-top: -100px; /* Jekyllのヘッダーを相殺 */
  z-index: 1;
  background-image: url('https://images.unsplash.com/photo-1514525253361-bee8718a340b?auto=format&fit=crop&w=1920&q=80');
}
.kakuly-hero-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.8));
  z-index: 2;
}
.kakuly-hero-content {
  position: relative;
  z-index: 3;
  width: 90%;
  max-width: 1100px;
  color: #fff;
  padding: 0 40px; /* 左右のパディングを確保 */
}
.kakuly-profile-overlay {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 20px;
}
.kakuly-profile-overlay img {
  border-radius: 20px;
  max-width: 200px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
.kakuly-profile-overlay h1, .kakuly-profile-overlay .name {
  font-size: 4rem;
  font-weight: 900;
  margin: 0;
  line-height: 1;
  text-shadow: 0 2px 20px rgba(0,0,0,0.5);
}
.kakuly-profile-overlay .links a {
    color: #fff;
    text-decoration: none;
    font-size: 1.5rem;
    margin-right: 15px;
    transition: opacity 0.3s;
}
.kakuly-profile-overlay .links a:hover { opacity: 0.7; }

/* 既存のJekyllラッパーを尊重するための調整 */
.wrapper {
    max-width: 1100px !important;
    padding-right: 40px !important;
    padding-left: 40px !important;
}
</style>

<div class="kakuly-hero-section">
  <div class="kakuly-hero-overlay"></div>
  <div class="kakuly-hero-content">
    <div class="kakuly-profile-overlay">
      <img src="https://pbs.twimg.com/profile_images/1879541331043364864/mYp7399t_400x400.jpg" alt="Kakuly">
      <h1 class="name">Kakuly</h1>
      <div class="links">
        <a href="https://soundcloud.com/kakuly" target="_blank">☁️</a>
        <a href="https://x.com/Kakuly_" target="_blank">X</a>
      </div>
    </div>
  </div>
</div>

<!-- ニュースセクションを挿入 -->

<!-- NEWS_START -->

<div class="news-section-wrapper">
  <h2 class="section-title">NEWS</h2>
  <div class="news-scroll-container">
    <div class="news-card" onclick="openNewsModal('1')">
      <div class="news-card-date">2026-01-23</div>
      <div class="news-card-title">ポートフォリオサイトをリニューアルしました</div>
      <div class="news-card-content-hidden" id="news-content-1" style="display:none;">ポートフォリオサイトのデザインを一新し、ニュースセクションを追加しました。今後はこちらで最新情報をお届けします。</div>
    </div>
    <div class="news-card" onclick="openNewsModal('2')">
      <div class="news-card-date">2026-01-20</div>
      <div class="news-card-title">新しい楽曲を公開しました</div>
      <div class="news-card-content-hidden" id="news-content-2" style="display:none;">YouTubeにて新しい制作楽曲を公開しました。ぜひWorksページからチェックしてください。</div>
    </div>
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
/* ニュースセクション専用スタイル */
.news-section-wrapper { margin: 40px 0; overflow: visible; position: relative; z-index: 10; }
.news-section-wrapper .section-title { font-family: 'Montserrat', sans-serif; font-size: 1.8rem; margin-bottom: 20px; letter-spacing: -0.05em; }
.news-scroll-container { 
  display: flex; 
  overflow-x: auto; 
  gap: 20px; 
  padding: 20px 5px;
  scrollbar-width: none;
  -ms-overflow-style: none;
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
.news-card:hover { 
  transform: translateY(-5px); 
  box-shadow: 0 10px 20px rgba(0,0,0,0.2); 
  border-color: var(--text-color);
}
.news-card-date { font-family: 'Montserrat', sans-serif; font-size: 0.75rem; opacity: 0.7; margin-bottom: 8px; }
.news-card-title { font-size: 1rem; font-weight: 700; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }

/* モーダル */
.modal { display: none; position: fixed; z-index: 100001; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.8); backdrop-filter: blur(10px); }
.modal-content { background-color: var(--bg-color); margin: 10% auto; padding: 40px; border-radius: 20px; width: 85%; max-width: 600px; position: relative; color: var(--text-color); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
.close-modal { color: var(--text-color); float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
.modal-date { font-family: 'Montserrat', sans-serif; font-size: 0.9rem; opacity: 0.5; margin-bottom: 10px; }
.modal-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 20px; line-height: 1.3; }
.modal-body { font-size: 1rem; line-height: 1.8; white-space: pre-wrap; }
</style>

<script>
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


<!-- 既存のAboutセクションをMarkdownで記述 -->
## About
2006年生まれ。2020年から音楽活動を開始。エレクトロポップ / ハイパーポップを中心に、たくさん迷いながら音楽を作っている。元気に生きるために音楽を摂取します。いつもありがとう。

## Contact
[DM on X](https://x.com/Kakuly_)
kakuly.work@gmail.com
