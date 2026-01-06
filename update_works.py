import os
import requests
import google.generativeai as genai

# 設定
API_KEY = os.environ['YOUTUBE_API_KEY']
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
PLAYLIST_ID = 'PLH9mX0wDlDAou_YCjcU01Q3pR6cCRQPWS'
FILE_PATH = 'works.md'

# Geminiの設定
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = None

def get_tags_from_ai(title, description):
    tags = []
    desc_and_title = (title + description).lower()
    
    # 1. まずキーワードで判定（確実なバックアップ）
    if any(k in desc_and_title for k in ['mix', 'ミックス', '混ぜ']):
        tags.append('Mix')
    if any(k in desc_and_title for k in ['arrang', '編曲', 'arrange']):
        tags.append('Arrangement')
    if any(k in desc_and_title for k in ['master', 'マスタリング']):
        tags.append('Mastering')
    if any(k in desc_and_title for k in ['movie', '映像', '動画']):
        tags.append('Movie')
    if any(k in desc_and_title for k in ['music', '作曲', '作詞']):
        tags.append('Music')
    
    # 2. AIが使える場合はAIで補完
    if model:
        prompt = f"""
        以下のYouTube動画のタイトルと概要欄から、制作者（Kakuly / かくり）が担当した役割を抽出してください。
        
        【抽出対象】Mix, Arrangement, Mastering, Movie, Music, Lyric
        
        【ルール】
        1. Kakuly / かくり 本人の担当のみ。他人は除外。
        2. 役割を英語で、カンマ区切りで返してください。該当なしは「None」。
        3. 余計な説明は一切不要。
        
        タイトル: {title}
        概要欄: {description}
        """
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()
            if result != "None":
                ai_tags = [t.strip() for t in result.split(',')]
                tags.extend(ai_tags)
        except:
            pass
            
    return list(set(tags)) # 重複削除

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

    # --- 3. 演出用パーツとデザイン（一切変更なし） ---
    content += '<div id="iris-in"></div>'
    content += '<div id="iris-out"></div>'
    content += """
<style>
.tag-container { margin-top: 10px; display: flex; flex-wrap: wrap; gap: 5px; }
.work-tag { font-size: 0.65rem; padding: 2px 8px; border-radius: 4px; border: 1px solid var(--text-color); opacity: 0.7; font-family: 'Montserrat', sans-serif; text-transform: uppercase; }
.video-thumbnail { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 12px; transition: transform 0.3s ease, box-shadow 0.3s ease; }
.video-link:hover .video-thumbnail { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
.video-title { margin-top: 10px; font-size: 1rem; font-weight: 600; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.wrapper { max-width: 1100px !important; padding-right: 40px !important; padding-left: 40px !important; }
.site-header .wrapper { max-width: 1100px !important; }
@import url('
