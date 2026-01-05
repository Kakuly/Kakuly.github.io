import os
import requests

# 設定
API_KEY = os.environ['YOUTUBE_API_KEY']
PLAYLIST_ID = 'PLH9mX0wDlDAou_YCjcU01Q3pR6cCRQPWS'
FILE_PATH = 'works.md'

def get_playlist_items():
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=20&playlistId={PLAYLIST_ID}&key={API_KEY}"
    response = requests.get(url).json()
    items = response.get('items', [])
    return items

def update_markdown(items):
    # --- 1. ヘッダー部分（元のまま） ---
    content = "---\nlayout: page\ntitle: Works\npermalink: /works/\n---\n\n"
    content += "### Music/Mix/Mastering/Movie\n\n"
    
    # 横並びにするための「外枠」を開始
    content += '<div class="video-grid">\n\n'
    
    # --- 2. 動画リスト部分（Kakulyさんの指定した構造） ---
    for item in items:
        title = item['snippet']['title']
        video_id = item['snippet']['resourceId']['videoId']
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        content += '<div class="video-item">\n'
        # サムネイル（リンク付き）
        content += f'  <a href="https://www.youtube.com/watch?v={video_id}" target="_blank" class="video-link">\n'
        content += f'    <img src="{thumbnail_url}" alt="{title}" class="video-thumbnail">\n'
        content += f'  </a>\n'
        # タイトル（下配置）
        content += f"  <h3 class='video-title'>{title}</h3>\n"
        content += '</div>\n\n'

    # 外枠を閉じる
    content += '</div>\n\n'

    # --- 3. 演出用パーツとデザイン（Kakulyさんのコードを完全維持） ---
    content += '<div id="iris-in"></div>'
    content += '<div id="iris-out"></div>'

    # ここから下は送っていただいた CSS と Script をそのまま流し込みます
    content += """
<style>
.video-thumbnail {
  width: 100%;
  aspect-ratio: 16 / 9; /* 比率を固定 */
  object-fit: cover;
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* マウスを乗せた時の演出 */
.video-link:hover .video-thumbnail {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.video-title {
  margin-top: 15px;
  font-size: 1rem;
  font-weight: 600;
  /* 2行目以降を「...」にする（タイトルが長い時用） */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

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

/* 4. ヘッダー・ナビゲーション */
.site-header { background-color: transparent !important; border: none !important; -webkit-font-smoothing: antialiased; }

h1, h2, h3, .site-title { 
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

/* 5. ギャラリー（4列）の設定 */
/* Worksの動画グリッドをより広々と見せる調整 */
.video-grid {
  display: grid !important;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)) !important;
  gap: 30px !important;
}

.video-item h3 {
  font-family: 'Montserrat', 'Noto Sans JP', sans-serif !important;
  font-size: 0.85rem !important;
  height: 3em;
  overflow: hidden;
  margin-bottom: 10px !important;
  line-height: 1.3;
}

/* 6. 不要な要素の削除 */
.rss-subscribe, .feed-icon, .site-footer { display: none !important; }

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

/* スマホ対応 */
@media (max-width: 800px) {
  .profile-container { flex-direction: column; align-items: flex-start; }
  .profile-name { font-size: 5rem !important; }
  .profile-icon { width: 200px; height: 200px; }
}

/* --- イン（入場）：穴が広がる演出 --- */
#iris-in {
  position: fixed;
  top: 50%; left: 50%;
  width: 10px; height: 10px;
  border-radius: 50%;
  box-shadow: 0 0 0 500vmax var(--bg-color);
  z-index: 100000;
  pointer-events: none;
  transform: translate(-50%, -50%) scale(0);
  transition: transform 1.2s cubic-bezier(0.85, 0, 0.15, 1);
}

body.is-opening #iris-in {
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

/* コンテンツの中身をフェードイン */
body > *:not([id^="iris-"]) {
  opacity: 0;
  transition: opacity 0.8s ease-out;
}

body.is-opening > *:not([id^="iris-"]) {
  opacity: 1;
  transition-delay: 0.2s;
}
</style>

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
    requestAnimationFrame(() => {
      setTimeout(() => {
        document.body.classList.add('is-opening');
      }, 50);
    });
  }

  window.addEventListener('pageshow', startIris);

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
"""

    # --- 4. 書き出し ---
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    items = get_playlist_items()
    if items:
        update_markdown(items)
        print("Successfully updated works.md")
