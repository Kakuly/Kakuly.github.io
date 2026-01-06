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
