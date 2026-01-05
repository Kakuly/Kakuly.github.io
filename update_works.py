import os
import requests

# 設定
API_KEY = os.environ['YOUTUBE_API_KEY']
PLAYLIST_ID = 'PLH9mX0wDlDAowW9zPkyOygWJXXzLcHDRN'
FILE_PATH = 'works.md'

def get_playlist_items():
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=20&playlistId={PLAYLIST_ID}&key={API_KEY}"
    response = requests.get(url).json()
    items = response.get('items', [])
    return items

def update_markdown(items):
    # ヘッダー部分
    content = "---\nlayout: page\ntitle: Works\npermalink: /works/\n---\n\n"
    content += "## YouTube Playlist (Auto Updated)\n\n"
    
    # 横並びにするための「外枠」を開始
    content += '<div class="video-grid">\n\n'
    
    for item in items:
        title = item['snippet']['title']
        video_id = item['snippet']['resourceId']['videoId']
        
        # 各動画を囲む「タイル」
        content += '<div class="video-item">\n'
        content += f"  <h3>{title}</h3>\n"
        # 埋め込みプレイヤーのコード
        content += f'  <iframe src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>\n'
        content += '</div>\n\n'
        
    # 外枠を閉じる
    content += '</div>\n\n'
    
    # デザイン設定（Homeと完全に同期）
    content += """
<style>
  /* 1. フォント読み込み */
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');

  /* 2. カラー変数設定 */
  :root {
    --bg-color: #ffffff;
    --text-color: #111111;
  }
  
  body.dark-mode {
    --bg-color: #000000;
    --text-color: #eeeeee;
  }

  /* 3. 全体レイアウト */
  body { 
    background-color: var(--bg-color) !important; 
    color: var(--text-color) !important; 
    transition: 0.3s;
    font-family: 'Noto Sans JP', sans-serif !important;
    -webkit-font-smoothing: antialiased;
  }

  /* 4. ヘッダー・ナビゲーション */
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

  /* 5. ギャラリー（4列）の設定 */
  .video-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)) !important;
    gap: 40px 20px !important;
    padding-top: 20px;
  }
  
  .video-item h3 {
    font-family: 'Montserrat', 'Noto Sans JP', sans-serif !important;
    font-size: 0.85rem !important;
    height: 3em;
    overflow: hidden;
    margin-bottom: 10px !important;
    line-height: 1.3;
  }
  
  iframe {
    width: 100% !important;
    aspect-ratio: 16 / 9;
    border-radius: 8px;
    background: #111;
    border: none;
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
    # ↑ この上のクォート3つが重要です！

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    items = get_playlist_items()
    if items:
        update_markdown(items)
        print("Successfully updated works.md")
