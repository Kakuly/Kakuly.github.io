import os
import requests
import google.generativeai as genai

# 設定
API_KEY = os.environ['YOUTUBE_API_KEY']
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
PLAYLIST_ID = 'PLH9mX0wDlDAou_YCjcU01Q3pR6cCRQPWS'
FILE_PATH = 'works.md'

# Geminiの設定
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

def get_tags_from_ai(title, description):
    """AIとキーワード検索を組み合わせてタグを抽出する"""
    tags = []
    
    # 1. まずはキーワード検索で確実なものを拾う（バックアップ用）
    text = (title + description).lower()
    keywords = {
        'Mix': ['mix', 'ミックス', '混ぜ'],
        'Arrangement': ['arrang', '編曲', 'arrange'],
        'Mastering': ['master', 'マスタリング'],
        'Movie': ['movie', '映像', '動画'],
        'Music': ['music', '作曲', '作詞'],
        'Lyric': ['lyric', '作詞']
    }
    for tag, keys in keywords.items():
        if any(k in text for k in keys):
            tags.append(tag)

    # 2. Gemini APIが使える場合はAIで詳細に判定
    if GEMINI_API_KEY:
        prompt = f"""
        以下のYouTube動画のタイトルと概要欄から、制作者（Kakuly / かくり）が担当した役割のみを抽出してください。
        
        【抽出対象】
        Mix, Arrangement, Mastering, Movie, Music, Lyric
        
        【ルール】
        1. Kakuly（かくり）本人の担当分のみを抽出。他人の担当は除外。
        2. 結果は英語でカンマ区切り（例: Mix, Mastering）。該当なしは「None」。
        3. 余計な説明は一切不要。
        
        タイトル: {title}
        概要欄: {description}
        """
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()
            if result != "None":
                # AIが抽出したタグを追加して重複を消す
                ai_tags = [t.strip() for t in result.split(',')]
                tags.extend(ai_tags)
        except:
            pass # AIエラー時はキーワード検索の結果のみ採用

    return list(set(tags)) # 重複を削除して返す

def get_playlist_items():
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=20&playlistId={PLAYLIST_ID}&key={API_KEY}"
    response = requests.get(url).json()
    return response.get('items', [])

def update_markdown(items):
    # --- 1. ヘッダー部分 ---
    content = "---\nlayout: page\ntitle: Works\npermalink: /works/\n---\n\n"
    content += "### Music / Mix / Mastering / Movie\n\n"
    content += '<div class="video-grid">\n\n'
    
    # --- 2. 動画リスト部分 ---
    for item in items:
        snippet = item['snippet']
        title = snippet['title']
        description = snippet['description']
        video_id = snippet['resourceId']['videoId']
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        tags = get_tags_from_ai(title, description)
        
        content += '<div class="video-item">\n'
        content += f'  <a href="https://www.youtube.com/watch?v={video_id}" target="_blank" class="video-link">\n'
        content += f'    <img src="{thumbnail_url}" alt="{title}" class="video-thumbnail" loading="lazy">\n'
        content += f'  </a>\n'
        
        if tags:
            content += '  <div class="tag-container">\n'
            for tag in tags:
                content += f'    <span class="work-tag">{tag}</span>\n'
            content += '  </div>\n'
            
        content += f"  <h3 class='video-title'>{title}</h3>\n"
        content += '</div>\n\n'

    content += '</div>\n\n'
    content += '<div id="iris-in"></div><div id="iris-out"></div>\n'

    # --- 3. デザインとスクリプト ---
    content += """
<style>
.tag-container { margin-top: 10px; display: flex; flex-wrap: wrap; gap: 5px; }
.work-tag { font-size: 0.65rem; padding: 2px 8px; border-radius: 4px; border: 1px solid var(--text-color); opacity: 0.7; font-family: 'Montserrat', sans-serif; text-transform: uppercase; }
.video-thumbnail { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 12px; transition: transform 0.3s ease, box-shadow 0.3s ease; }
.video-link:hover .video-thumbnail { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
.video-title { margin-top: 10px; font-size: 1rem; font-weight: 600; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.wrapper { max-width: 1100px !important; padding: 0 40px !important; }
.site-header .wrapper { max-width: 1100px !important; }
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');
:root { --bg-color: #ffffff; --text-color: #111111; }
html.dark-mode, body.dark-mode { --bg-color: #000000; --text-color: #eeeeee; background-color: #000000 !important; }
body { background-color: var(--bg-color) !important; color: var(--text-color) !important; font-family: 'Noto Sans JP', sans-serif !important; font-weight: 700 !important; }
.video-grid { display: grid !important; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)) !important; gap: 30px !important; }
.rss-subscribe, .feed-icon, .site-footer { display: none !important; }
#mode-toggle { cursor: pointer; background: none; border: 1px solid var(--text-color); color: var(--text-color); padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; position: fixed; top: 15px; right: 20px; z-index: 9999; font-weight: bold; }
#iris-in { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 0 500vmax var(--bg-color); z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 1.2s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-opening #iris-in { transform: translate(-50%, -50%) scale(500); }
#iris-out { position: fixed; top: 50%; left: 50%; width: 150vmax; height: 150vmax; background-color: var(--bg-color); border-radius: 50%; z-index: 100001; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 0.8s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-exiting #iris-out { transform: translate(-50%, -50%) scale(1.2) !important; }
body > *:not([id^="iris-"]) { opacity: 0; transition: opacity 0.8s ease-out; }
body.is-opening > *:not([id^="iris-"]) { opacity: 1; transition-delay: 0.2s; }
</style>
<button id="mode-toggle">🌙 Dark Mode</button>
<script>
  const btn = document.getElementById('mode-toggle');
  const body = document.body;
  const html = document.documentElement;
  if (localStorage.getItem('theme') === 'dark') { html.classList.add('dark-mode'); body.classList.add('dark-mode'); btn.textContent = '☀️ Light Mode'; }
  btn.addEventListener('click', () => { body.classList.add('mode-transition'); const isDark = html.classList.toggle('dark-mode'); body.classList.toggle('dark-mode'); localStorage.setItem('theme', isDark ? 'dark' : 'light'); btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode'; setTimeout(() => { body.classList.remove('mode-transition'); }, 500); });
  function startIris() { document.body.classList.remove('is-opening', 'is-exiting'); requestAnimationFrame(() => { setTimeout(() => { document.body.classList.add('is-opening'); }, 50); }); }
  window.addEventListener('pageshow', startIris);
  document.querySelectorAll('a').forEach(link => { link.addEventListener('click', (e) => { const href = link.getAttribute('href'); if (!href || href.startsWith('#') || href.includes('mailto:') || link.target === "_blank") return; e.preventDefault(); document.body.classList.add('is-exiting'); setTimeout(() => { window.location.href = href; }, 800); }); });
</script>
"""

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    items = get_playlist_items()
    if items:
        update_markdown(items)
        print("Successfully updated works.md with hybrid AI tags")
