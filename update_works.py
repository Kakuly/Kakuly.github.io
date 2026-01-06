import os
import json
import requests
import google.generativeai as genai
import html

# --- 設定 ---
API_KEY = os.environ['YOUTUBE_API_KEY']
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
PLAYLIST_ID = 'PLH9mX0wDlDAou_YCjcU01Q3pR6cCRQPWS'
FILE_PATH = 'works.md'
CACHE_FILE = 'known_works.json'

# --- JSONキャッシュの読み込み/作成 ---
def load_known_works():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_known_works(data):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 起動時に読み込み
KNOWN_WORKS = load_known_works()

# Geminiの設定
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        for m_name in ['gemini-2.0-flash', 'gemini-1.5-flash']:
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

def get_tags(video_id, title, description):
    if video_id in KNOWN_WORKS:
        cached_data = KNOWN_WORKS[video_id]
        if isinstance(cached_data, dict):
            tags_in_cache = cached_data.get("tags", [])
            if len(tags_in_cache) > 0 and "None" not in tags_in_cache:
                return tags_in_cache

    past_examples = ""
    example_count = 0
    for k, v in KNOWN_WORKS.items():
        if isinstance(v, dict) and v.get("tags"):
            past_examples += f"- {v['title']}: {', '.join(v['tags'])}\n"
            example_count += 1
            if example_count > 15: break

    tags = []
    if model:
        prompt = f"""
        あなたは楽曲クレジットの専門家です。ネット検索を行い、以下の動画における「Kakuly（かくり）」の正確な担当役割を特定してください。
        
        【参考：Kakulyの過去の実績傾向】
        {past_examples}
        【今回の動画】
        動画タイトル: {title}
        概要欄抜粋: {description[:500]}
        
        【出力形式】
        英語のタグのみをカンマ区切りで。該当なしは「None」。
        """
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()
            if result != "None" and len(result) > 1:
                tags = [t.strip() for t in result.split(',')]
        except: pass

    if not tags:
        l_lower = (title + "\n" + description).lower()
        patterns = [('mix', 'Mix'), ('編曲', 'Arrangement'), ('master', 'Mastering'),
                    ('movie', 'Movie'), ('映像', 'Movie'), ('music', 'Music'),
                    ('作曲', 'Music'), ('lyric', 'Lyrics'), ('作詞', 'Lyrics'), ('remix', 'Remix')]
        for pat, val in patterns:
            if pat in l_lower: tags.append(val)
    
    processed_tags = sorted(list(set([t.replace('Lyric', 'Lyrics') if t == 'Lyric' else t for t in tags])))
    KNOWN_WORKS[video_id] = {"title": title, "tags": processed_tags}
    save_known_works(KNOWN_WORKS)
    return processed_tags

def get_playlist_items():
    all_items = []
    next_page_token = None
    while True:
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={PLAYLIST_ID}&key={API_KEY}"
        if next_page_token: url += f"&pageToken={next_page_token}"
        try:
            r = requests.get(url).json()
            items = r.get('items', [])
            all_items.extend(items)
            next_page_token = r.get('nextPageToken')
            if not next_page_token: break
        except: break
    return all_items

def update_markdown(items):
    content = "---\nlayout: page\ntitle: Works\npermalink: /works/\n---\n\n"
    
    # フィルタボタンコンテナ
    content += '<div id="filter-container" class="filter-wrapper"></div>\n\n'
    content += '<div class="video-grid" id="video-grid">\n\n'
    
    for item in items:
        snippet = item['snippet']
        raw_title = snippet['title']
        title = html.escape(raw_title)
        description = snippet['description']
        video_id = snippet['resourceId']['videoId']
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        tags = get_tags(video_id, title, description)
        tags_attr = ",".join(tags) if tags else ""
        
        # 既存の構造を維持しつつ、ソート用属性を付与
        content += f'<div class="video-item" data-tags="{tags_attr}">\n'
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
    
    # 演出用パーツ
    content += '<div id="iris-in"></div>'
    content += '<div id="iris-out"></div>'

    content += """
<style>
/* --- フィルタUI --- */
.filter-wrapper {
  margin-bottom: 40px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.filter-btn {
  cursor: pointer;
  font-family: 'Montserrat', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.9rem;
  padding: 6px 16px;
  border-radius: 30px;
  border: 1px solid var(--text-color);
  background: transparent;
  color: var(--text-color);
  transition: all 0.3s ease;
  text-transform: uppercase;
  opacity: 0.3;
}
.filter-btn.active {
  opacity: 1;
  background: var(--text-color);
  color: var(--bg-color);
}

/* --- ソートアニメーション用 --- */
.video-item {
  transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1), transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  transform: scale(1);
  opacity: 1;
}
.video-item.sort-hide {
  opacity: 0;
  transform: scale(0.95);
  pointer-events: none;
  position: absolute; /* レイアウトを詰めさせるための設定 */
  visibility: hidden;
}

/* --- 元のデザイン設定 (完全維持) --- */
.tag-container { margin-top: 4px; display: flex; flex-wrap: wrap; gap: 5px; }
.work-tag { font-size: 0.57rem; padding: 1px 6px; border-radius: 4px; border: 0.5px solid var(--text-color); opacity: 0.88; font-family: 'Montserrat', sans-serif; text-transform: uppercase; }
.video-thumbnail { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 12px; transition: transform 0.3s ease, box-shadow 0.3s ease; }
.video-link:hover .video-thumbnail { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
.video-title { margin-top: 10px; font-size: 1rem; font-weight: 600; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 0px !important; font-family: 'Noto Sans JP', sans-serif !important; }
.wrapper { max-width: 1100px !important; padding-right: 40px !important; padding-left: 40px !important; }
.site-header .wrapper { max-width: 1100px !important; }
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');
:root { --bg-color: #ffffff; --text-color: #111111; }
html.dark-mode, body.dark-mode { --bg-color: #000000; --text-color: #eeeeee; background-color: #000000 !important; }
body { background-color: var(--bg-color) !important; color: var(--text-color) !important; transition: none !important; font-family: 'Noto Sans JP', sans-serif !important; font-weight: 700 !important; }
body.mode-transition { transition: background-color 0.5s ease, color 0.5s ease !important; }
.site-header { background-color: transparent !important; border: none !important; }
h1, h2, h3, .site-title { font-family: 'Montserrat', sans-serif !important; font-size: 1.4rem !important; font-weight: 700 !important; letter-spacing: -0.05em !important; color: var(--text-color) !important; }
.page-link { font-family: 'Montserrat', sans-serif !important; color: var(--text-color) !important; font-weight: 700 !important; text-transform: uppercase; font-size: 0.9rem !important; margin-left: 20px !important; text-decoration: none !important; }
.video-grid { display: grid !important; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)) !important; gap: 60px 40px !important; position: relative; }
.video-item h3 { font-family: 'Noto Sans JP', sans-serif !important; font-size: 0.85rem !important; height: auto !important; min-height: 1.3em; overflow: hidden; margin-bottom: 0px !important; line-height: 1.3; }
.rss-subscribe, .feed-icon, .site-footer { display: none !important; }
#mode-toggle { cursor: pointer; background: none; border: 1px solid var(--text-color); color: var(--text-color); padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; position: fixed; top: 15px; right: 20px; z-index: 9999; font-weight: bold; }
/* モバイル対応：画面幅が768px以下の時（スマホなど） */
@media screen and (max-width: 1100px) {
  #mode-toggle {
    top: auto !important;   /* 上固定を解除 */
    bottom: 20px !important; /* 下から20pxの位置に */
    right: 20px !important;
  }
}
#iris-in { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 0 500vmax var(--bg-color); z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 1.2s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-opening #iris-in { transform: translate(-50%, -50%) scale(500); }
#iris-out { position: fixed; top: 50%; left: 50%; width: 150vmax; height: 150vmax; background-color: var(--bg-color); border-radius: 50%; z-index: 100001; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 0.8s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-exiting #iris-out { transform: translate(-50%, -50%) scale(1.2) !important; }
body > *:not([id^="iris-"]) { opacity: 0; transition: opacity 0.8s ease-out; }
body.is-opening > *:not([id^="iris-"]) { opacity: 1; transition-delay: 0.2s; }
</style>

<button id="mode-toggle">🌙 Dark Mode</button>

<script>
  document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('video-grid');
    const items = Array.from(grid.querySelectorAll('.video-item'));
    const filterContainer = document.getElementById('filter-container');
    const activeFilters = new Set();

    const allTags = new Set();
    items.forEach(item => {
      const tags = item.dataset.tags.split(',').filter(t => t);
      tags.forEach(t => allTags.add(t));
    });

    Array.from(allTags).sort().forEach(tag => {
      const btn = document.createElement('button');
      btn.className = 'filter-btn';
      btn.textContent = tag;
      btn.onclick = () => {
        btn.classList.toggle('active');
        if (activeFilters.has(tag)) activeFilters.delete(tag);
        else activeFilters.add(tag);
        applyFilter();
      };
      filterContainer.appendChild(btn);
    });

    function applyFilter() {
      items.forEach(item => {
        const itemTags = item.dataset.tags.split(',');
        const isVisible = activeFilters.size === 0 || Array.from(activeFilters).some(f => itemTags.includes(f));
        
        if (isVisible) {
          item.classList.remove('sort-hide');
          item.style.position = 'relative';
          item.style.pointerEvents = 'auto';
          item.style.visibility = 'visible';
        } else {
          item.classList.add('sort-hide');
          setTimeout(() => {
            if (item.classList.contains('sort-hide')) {
              item.style.position = 'absolute';
            }
          }, 400);
        }
      });
    }
  });

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
    setTimeout(() => { body.classList.remove('mode-transition'); }, 500);
  });
  
  function startIris() {
    document.body.classList.remove('is-opening', 'is-exiting');
    requestAnimationFrame(() => {
      setTimeout(() => { document.body.classList.add('is-opening'); }, 50);
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
