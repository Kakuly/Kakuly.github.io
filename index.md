---
layout: home
title: Home
---

<div class="hero-section" style="background-image: url('');">
  <div class="hero-overlay"></div>
  <div class="hero-content">
    
<!-- NEWS_START -->
<div class="news-section">
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
/* ニュースセクション */
.news-section { margin: 40px 0; overflow: visible; position: relative; z-index: 10; }
.section-title { font-family: 'Montserrat', sans-serif; font-size: 1.8rem; margin-bottom: 20px; letter-spacing: -0.05em; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }
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
  background: rgba(255, 255, 255, 0.1); 
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2); 
  border-radius: 15px; 
  padding: 20px; 
  cursor: pointer; 
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  color: #fff;
}
.news-card:hover { 
  transform: translateY(-10px); 
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 15px 30px rgba(0,0,0,0.3); 
  border-color: rgba(255, 255, 255, 0.5);
}
.news-card-date { font-family: 'Montserrat', sans-serif; font-size: 0.75rem; opacity: 0.7; margin-bottom: 8px; }
.news-card-title { font-size: 1rem; font-weight: 700; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }

/* モーダル */
.modal { display: none; position: fixed; z-index: 100001; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.8); backdrop-filter: blur(10px); }
.modal-content { background-color: var(--bg-color); margin: 10% auto; padding: 40px; border-radius: 20px; width: 85%; max-width: 600px; position: relative; color: var(--text-color); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
.close-modal { position: absolute; right: 25px; top: 20px; font-size: 28px; font-weight: bold; cursor: pointer; opacity: 0.5; }
.close-modal:hover { opacity: 1; }
.modal-date { font-family: 'Montserrat', sans-serif; font-size: 0.9rem; opacity: 0.5; margin-bottom: 10px; }
.modal-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 20px; line-height: 1.3; }
.modal-body { font-size: 1rem; line-height: 1.8; white-space: pre-wrap; }

/* ヘッダー画像とオーバーレイ */
.hero-section {
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
  margin-top: -100px;
  z-index: 1;
}
.hero-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.8));
  z-index: 2;
}
.hero-content {
  position: relative;
  z-index: 3;
  width: 90%;
  max-width: 1100px;
  color: #fff;
}

/* セクション背景 */
.content-section {
  position: relative;
  width: 100vw;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  padding: 100px 0;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  z-index: 1;
}
.section-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 40px;
  position: relative;
  z-index: 3;
}
</style>

<script>
function openNewsModal(id) {
  const card = document.querySelector(`#news-content-${id}`).parentElement;
  const title = card.querySelector('.news-card-title').innerText;
  const date = card.querySelector('.news-card-date').innerText;
  const content = document.getElementById(`news-content-${id}`).innerText;
  document.getElementById('modal-title').innerText = title;
  document.getElementById('modal-date').innerText = date;
  document.getElementById('modal-body').innerText = content;
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

    <div class="profile-overlay">
      </div>
    </div>
  </div>
</div>

  </div>
</div>
    </div>
  </div>
</div>

<div class="content-section">
  <div class="section-inner">
    
  </div>
</div>

<style>
.profile-overlay {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 20px;
}
/* 元のアイコンや名前のスタイルを維持するための調整 */
.profile-overlay img {
  border-radius: 20px;
  max-width: 200px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
.profile-overlay h1, .profile-overlay .name {
  font-size: 4rem;
  font-weight: 900;
  margin: 0;
  line-height: 1;
  text-shadow: 0 2px 20px rgba(0,0,0,0.5);
}
</style>
