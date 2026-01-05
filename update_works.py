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
    
    # 前回のデザイン設定（style）をそのまま残す
    content += """
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


  /* 2. フォントを「ダサくない」モダンなものに変える */
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');
  body, p, li { font-family: 'Noto Sans JP', sans-serif !important; line-height: 1.8; letter-spacing: -0.03em !important; }
  .site-title, h1, h2, h3 { font-family: 'Montserrat', sans-serif !important; font-weight: 700:  !important; letter-spacing: -0.03em !important; }
  
  /* タイル状に並べる設定（横4つ） */
  .video-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)) !important;
    gap: 40px 20px !important;
    padding-top: 20px;
  }
  
  .video-item h3 {
    font-size: 0.85rem !important;
    height: 3em;
    overflow: hidden;
    margin-bottom: 10px !important;
  }
  
  iframe {
    width: 100% !important;
    aspect-ratio: 16 / 9;
    border-radius: 8px;
    background: #111;
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
"""
        
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    items = get_playlist_items()
    if items:
        update_markdown(items)
        print("Successfully updated works.md with embedded players")
