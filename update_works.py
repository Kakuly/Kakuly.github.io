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
  
  .site-title { 
    font-family: 'Montserrat', sans-serif !important;
    font-size: 1.4rem !important; 
    font-weight: 700 !important;
    letter-spacing: -0.05em !important;
    color: var(--text-color) !important;
  }

  .page-link {
    font-family: 'Montserrat', sans-serif
