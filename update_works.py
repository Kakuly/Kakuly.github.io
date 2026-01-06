import os
import json
import requests
import google.generativeai as genai
import html # タイトルの混同を避けるためのインポート

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
    content = "--- \nlayout: page\ntitle: Works\npermalink: /works/\n---\n\n"
    
    # フィルタ用のタグコンテナ（空の状態で出力し、JSで中身を生成）
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
        # JSでフィルタリングするために data-tags 属性を付与
        tags_attr = ",".join(tags) if tags else ""
        
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
    content += '<div id="iris-in"></div><div id="iris-out"></div>'

    # --- デザインCSS（フィルタ用スタイルを追加） ---
    content += """
<style>
/* フィルタボタンのスタイル */
.filter-wrapper {
  margin-bottom: 40px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.filter-btn {
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  font-size: 0.9rem;
  padding: 6px 16px;
  border-radius: 30px;
  border: 1px solid var(--text-color);
  background: transparent;
  color: var(--text-color);
  transition: all 0.3s ease;
  text-transform: uppercase;
  opacity: 0.4; /* デフォルト（オフ）は薄く */
}
.filter-btn.active {
  opacity: 1; /* オンは濃く */
  background: var(--text-color);
  color: var(--bg-color);
}
.filter-btn:hover {
  opacity: 0.8;
}

/* 既存スタイル維持 */
.tag-container { margin-top: 4px; display: flex; flex-wrap: wrap; gap: 5px; }
.work-tag { font-size: 0.57rem; padding: 1px 6px; border-radius: 4px; border: 0.5px solid var(--text-color); opacity: 0.88; font-family: 'Montserrat', sans-serif; text-transform: uppercase; }
.video-thumbnail { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 12px; transition: transform 0.3s ease, box-shadow 0.3s ease; }
.video-link:hover .video-thumbnail { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
.video-title { margin-top: 10px; font-size: 1rem; font-weight: 600; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 0px !important; font-family: 'Noto Sans JP', sans-serif !important; }
.wrapper { max-width: 1100px !important; padding: 0 40px !important; }
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');
:root { --bg-color: #ffffff; --text-color: #111111; }
html.dark-mode, body.dark-mode { --bg-color: #000000; --text-color: #eeeeee; background-color: #000000 !important; }
body { background-color: var(--bg-color) !important; color: var(--text-color) !important; font-family: 'Noto Sans JP', sans-serif !important; font-weight: 700 !important; }
.video-grid { display: grid !important; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)) !important; gap: 60px 40px !important; }
.video-item { transition: opacity 0.4s ease, transform 0.4s ease; }
.video-item.hidden { display: none; }
.site-header { background-color: transparent !important; border: none !important; }
h1, h2, h3, .site-title { font-family: 'Montserrat', sans-serif !important; color: var(--text-color) !important; }
#mode-toggle { cursor: pointer; background: none; border: 1px solid var(--text-color); color: var(--text-color); padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; position: fixed; top: 15px; right: 20px; z-index: 9999; font-weight: bold; }
#iris-in, #iris-out { position: fixed; top: 50%; left: 50%; border-radius: 50%; pointer-events: none; z-index: 100000; transform: translate(-50%, -50%) scale(0); }
#iris-in { width: 10px; height: 10px; box-shadow: 0 0 0 500vmax var(--bg-color); transition: transform 1.2s cubic-bezier(0.85, 0, 0.15, 1); }
#iris-out { width: 150vmax; height: 150vmax; background-color: var(--bg-color); transition: transform 0.8s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-opening #iris-in { transform: translate(-50%, -50%) scale(500); }
body.is-exiting #iris-out { transform: translate(-50%, -50%) scale(1.2) !important; }
</style>

<button id="mode-toggle">🌙 Dark Mode</button>

<script>
  // --- フィルタリング機能 ---
  document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('video-grid');
    const items = Array.from(grid.querySelectorAll('.video-item'));
    const filterContainer = document.getElementById('filter-container');
    
    // 全タグを抽出
    const allTags = new Set();
    items.forEach(item => {
      const tags = item.dataset.tags.split(',').filter(t => t);
      tags.forEach(t => allTags.add(t));
    });

    // フィルタボタン生成
    const activeFilters = new Set();
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
        if (activeFilters.size === 0) {
          item.classList.remove('hidden');
          return;
        }
        const itemTags = item.dataset.tags.split(',');
        const hasMatch = Array.from(activeFilters).some(f => itemTags.includes(f));
        if (hasMatch) item.classList.remove('hidden');
        else item.classList.add('hidden');
      });
    }
  });

  // --- ダークモード / 演出 (既存維持) ---
  const btn = document.getElementById('mode-toggle');
  const htmlEl = document.documentElement;
  if (localStorage.getItem('theme') === 'dark') { htmlEl.classList.add('dark-mode'); document.body.classList.add('dark-mode'); btn.textContent = '☀️ Light Mode'; }
  btn.addEventListener('click', () => {
    const isDark = html_el.classList.toggle('dark-mode');
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
  });
  window.addEventListener('pageshow', () => {
    document.body.classList.remove('is-opening', 'is-exiting');
    requestAnimationFrame(() => setTimeout(() => document.body.classList.add('is-opening'), 50));
  });
</script>
"""

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    items = get_playlist_items()
    if items:
        update_markdown(items)
        print(f"Total {len(items)} processed. Filtering UI updated.")
