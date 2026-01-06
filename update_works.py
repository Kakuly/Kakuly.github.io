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
        for m_name in ['gemini-2.0-flash', 'gemini-3.0-flash', 'gemini-1.5-flash']:
            try:
                model = genai.GenerativeModel(
                    model_name=m_name,
                    tools=[{'google_search_retrieval': {}}]
                )
                break
            except:
                continue
    except:
        model = None

def get_tags_from_ai(title, description):
    if model:
        prompt = f"""
        あなたは楽曲クレジットの専門家です。ネット検索を行い、以下の動画における「Kakuly（かくり）」の正確な担当役割を特定してください。
        
        動画タイトル: {title}
        概要欄抜粋: {description[:500]}

        【検索,特定の指示】
        1. Google検索でこの動画のクレジット（X, YouTube, 楽曲データベース）を調べてください。
        2. 「Kakuly」または「かくり」が担当した役割（Mix, Arrangement, Mastering, Movie, Music, Lyrics, Remix）を特定してください。
        3. 他人の担当（例: Vocal: ○○, Illust: △△）は絶対に除外してください。
        4. XFD作品は、高確率でXFD映像を作っているか、そのアルバムにオリジナル曲orリミックス　またはその両方で参加している可能性が高いです。
        5. アルバムに参加している場合にも、Musicに割り振ってください
        6. 基本的には概要欄やタイトルを参照し、不十分である場合検索をしっかりとかけてください
        7. タグがないことはありえません。
        8. MixとRemixは全く別物です、かつ同時につくことはほとんどないです。
        
        【出力形式】
        英語のタグのみをカンマ区切りで。該当なしは「None」。
        """
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()
            if result != "None" and len(result) > 1:
                return [t.strip() for t in result.split(',')]
        except:
            pass

    tags = []
    lines = (title + "\n" + description).split('\n')
    for line in lines:
        l_lower = line.lower()
        if 'kakuly' in l_lower or 'かくり' in l_lower:
            if any(k in l_lower for k in ['mix', 'ミックス']): tags.append('Mix')
            if any(k in l_lower for k in ['arrang', '編曲']): tags.append('Arrangement')
            if any(k in l_lower for k in ['master', 'マスタリング']): tags.append('Mastering')
            if any(k in l_lower for k in ['movie', '映像', '動画']): tags.append('Movie')
            if any(k in l_lower for k in ['music', '作曲']): tags.append('Music')
            if any(k in l_lower for k in ['lyric', '作詞']): tags.append('Lyric')
            if any(k in l_lower for k in ['remix', 'リミックス']): tags.append('Remix')
            
    return list(set(tags))

def get_playlist_items():
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=20&playlistId={PLAYLIST_ID}&key={API_KEY}"
    try:
        r = requests.get(url).json()
        return r.get('items', [])
    except:
        return []

def update_markdown(items):
    content = "--- \nlayout: page\ntitle: Works\npermalink: /works/\n---\n\n"
    content += "### Music / Mix / Mastering / Movie\n\n"
    content += '<div class="video-grid">\n\n'
    
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

        content += f"  <h3 class='video-title'>{title}</h3>"
        
        if tags:
            content += '  <div class="tag-container">\n'
            for tag in tags:
                content += f'    <span class="work-tag">{tag}</span>\n'
            content += '  </div>\n'
        content += '</div>\n\n'

    content += '</div>\n\n'
    content += '<div id="iris-in"></div>'
    content += '<div id="iris-out"></div>'

    content += """
<style>
.tag-container {
  margin-top: 2px; /* タイトルとの隙間を最小限に */
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}
.work-tag {
  font-size: 0.57rem;
  padding: 1px 6px;
  border-radius: 4px;
  border: 0.5px solid var(--text-color);
  opacity: 0.88;
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
  margin-top: 10px;
  font-size: 1rem;
  font-weight: 600;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 0px !important; /* 下の余白を強制的に消去 */
}

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
  height: 2.6em; /* 余白を削るため高さを少し詰め */
  overflow: hidden;
  margin-bottom: 0px !important; /* 下の余白を削除 */
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

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    items = get_playlist_items()
    if items:
        update_markdown(items)
        print("Successfully updated works.md with minimal tag gaps")
