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
        # まずは 3.0 Flash を試し、エラーなら 2.0 や 1.5 へ
        for model_name in ['gemini-3.0-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    tools=[{'google_search_retrieval': {}}]
                )
                # 試しに空のコンテンツを送ってモデルが有効か確認
                print(f"Using model: {model_name}")
                break 
            except:
                continue
    except Exception as e:
        print(f"Initial setup error: {e}")

def get_tags_from_ai(title, description):
    tags = []
    
    # 1. AI判定（ウェブ検索による裏取り付き）
    if model:
        prompt = f"""
            以下のYouTube動画について、ネット検索を活用して「Kakuly（かくり）」という人物が実際に担当した役割を特定してください。
            
            【対象動画】
            タイトル: {title}
            
            【判定のルール】
            1. 概要欄の情報だけでなく、必要に応じてこの動画のクレジット情報をネットで検索して確認してください。
            2. 「Kakuly / かくり」本人が担当した役割（Mix, Arrangement, Mastering, Movie, Music, Lyric）のみを抽出してください。
            3. 他のクリエイターの担当役割は絶対に含めないでください。
            4. 役割を英語で、カンマ区切りで返してください（例: Mix, Mastering）。
            5. 確証がない、または担当が不明な場合は「None」とだけ返してください。
            6. 余計な解説は不要です。
        """
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()
            if result != "None" and result != "":
                return [t.strip() for t in result.split(',')]
        except:
            pass

    # 2. バックアップ：AIが失敗した時の簡易キーワード判定
    text = (title + description).lower()
    if 'kakuly' in text or 'かくり' in text:
        if any(k in text for k in ['mix', 'ミックス']): tags.append('Mix')
        if any(k in text for k in ['arrang', '編曲', 'arrange']): tags.append('Arrangement')
        if any(k in text for k in ['master', 'マスタリング']): tags.append('Mastering')
        if any(k in text for k in ['movie', '映像', '動画']): tags.append('Movie')
        if any(k in text for k in ['music', '作曲']): tags.append('Music')
            
    return list(set(tags))

def get_playlist_items():
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=20&playlistId={PLAYLIST_ID}&key={API_KEY}"
    try:
        response = requests.get(url).json()
        return response.get('items', [])
    except:
        return []

def update_markdown(items):
    # ヘッダー
    content = "--- \nlayout: page\ntitle: Works\npermalink: /works/\n---\n\n"
    content += "### Music / Mix / Mastering / Movie\n\n"
    content += '<div class="video-grid">\n\n'
    
    # 動画リスト
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

    # --- デザイン・演出パーツ（ここから下は一切変更していません） ---
    content += '<div id="iris-in"></div>'
    content += '<div id="iris-out"></div>'
    content += """
<style>
/* 追加したタグのスタイル */
.tag-container {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}
.work-tag {
  font-size: 0.65rem;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid var(--text-color);
  opacity: 0.7;
  font-family: 'Montserrat', sans-serif;
  text-transform: uppercase;
}

.video-thumbnail {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.video-link:hover .video-thumbnail {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.video-title {
  margin-top: 10px; /* タグがある分少し調整 */
  font-size: 1rem;
  font-weight: 600;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* サイト全体の最大幅を上書き */
.wrapper {
  max-width: 1100px !important;
  padding-right: 40px !important;
  padding-left: 40px !important;
}

.site-header .wrapper {
  max-width: 1100px !important;
}

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');

:root {
  --bg-color: #ffffff;
  --text-color: #111111;
}

html.dark-mode, body.dark-mode {
  --bg-color: #000000;
  --text-color: #eeeeee;
  background-color: #000000 !important;
}

body { 
  background-color: var(--bg-color) !important; 
  color: var(--text-color) !important; 
  transition: none !important; 
  font-family: 'Noto Sans JP', sans-serif !important;
  font-weight: 700 !important;
}

body.mode-transition {
  transition: background-color 0.5s ease, color 0.5s ease !important;
}

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
  text-transform: uppercase;
  font-size: 0.9rem !important;
  margin-left: 20px !important;
  text-decoration: none !important;
}

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

.rss-subscribe, .feed-icon, .site-footer { display: none !important; }

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
}

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
    # 書き出し
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    items = get_playlist_items()
    if items:
        update_markdown(items)
        print("Successfully updated works.md with Search-based AI tags")
