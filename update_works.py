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

def load_known_works():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

def save_known_works(data):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

KNOWN_WORKS = load_known_works()

model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        for m_name in ['gemini-2.0-flash', 'gemini-1.5-flash']:
            try:
                model = genai.GenerativeModel(model_name=m_name, tools=[{'google_search_retrieval': {}}])
                break
            except: continue
    except: model = None

def get_tags(video_id, title, description):
    if video_id in KNOWN_WORKS:
        cached_data = KNOWN_WORKS[video_id]
        if isinstance(cached_data, dict):
            tags_in_cache = cached_data.get("tags", [])
            if len(tags_in_cache) > 0 and "None" not in tags_in_cache: return tags_in_cache
    
    past_examples = ""
    for k, v in list(KNOWN_WORKS.items())[:15]:
        if isinstance(v, dict) and v.get("tags"):
            past_examples += f"- {v['title']}: {', '.join(v['tags'])}\n"

    tags = []
    if model:
        prompt = f"あなたは楽曲クレジットの専門家です。ネット検索を行い、以下の動画における「Kakuly（かくり）」の正確な担当役割を特定してください。\n\n【参考：Kakulyの過去の実績傾向】\n{past_examples}\n【今回の動画】\n動画タイトル: {title}\n概要欄抜粋: {description[:500]}\n\n【出力形式】\n英語のタグのみをカンマ区切りで。該当なしは「None」。"
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()
            if result != "None" and len(result) > 1: tags = [t.strip() for t in result.split(',')]
        except: pass
    if not tags:
        l_lower = (title + "\n" + description).lower()
        patterns = [('mix', 'Mix'), ('編曲', 'Arrangement'), ('master', 'Mastering'), ('movie', 'Movie'), ('映像', 'Movie'), ('music', 'Music'), ('作曲', 'Music'), ('lyric', 'Lyrics'), ('作詞', 'Lyrics'), ('remix', 'Remix')]
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
            if not items: break
            all_items.extend(items)
            next_page_token = r.get('nextPageToken')
            if not next_page_token: break
        except: break
    return all_items

def update_markdown(items):
    # Front Matter (絶対に \n を直接書く)
    content = "---\nlayout: page\ntitle: Works\npermalink: /works/\n---\n\n"
    
    content += '<div id="filter-container" class="filter-wrapper"></div>\n\n'
    content += '<div class="video-grid" id="video-grid">\n'
    
    for item in items:
        snippet = item['snippet']
        title = html.escape(snippet['title'])
        video_id = snippet['resourceId']['videoId']
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        tags = get_tags(video_id, title, snippet['description'])
        tags_attr = ",".join(tags) if tags else ""
        
        content += f'  <div class="video-item" data-tags="{tags_attr}">\n'
        content += f'    <a href="https://www.youtube.com/watch?v={video_id}" target="_blank" class="video-link">\n'
        content += f'      <img src="{thumbnail_url}" alt="{title}" class="video-thumbnail" loading="lazy">\n'
        content += f'    </a>\n'
        content += f"    <h3 class='video-title'>{title}</h3>\n"
        if tags:
            content += '    <div class="tag-container">\n'
            for tag in tags: content += f'      <span class="work-tag">{tag}</span>\n'
            content += '    </div>\n'
        content += '  </div>\n'

    content += '</div>\n\n'
    content += '<div id="iris-in"></div><div id="iris-out"></div>\n'
    content += '<div id="loading-overlay">\n'
    content += '  <video id="loading-video-black" src="/loading_black.webm" autoplay loop muted playsinline class="loading-vid"></video>\n'
    content += '  <video id="loading-video-white" src="/loading_white.webm" autoplay loop muted playsinline class="loading-vid"></video>\n'
    content += '</div>\n'

    content += r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');
:root { --bg-color: #ffffff; --text-color: #111111; }
html.dark-mode { --bg-color: #000000; --text-color: #eeeeee; }
body { background-color: var(--bg-color) !important; color: var(--text-color) !important; font-family: 'Noto Sans JP', sans-serif !important; font-weight: 700 !important; margin: 0; }

#loading-overlay { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 100002; opacity: 0; pointer-events: none; transition: opacity 0.3s ease; }
.loading-vid { width: 120px; height: auto; display: none; }
#loading-video-black { display: block; }
html.dark-mode #loading-video-black { display: none; }
html.dark-mode #loading-video-white { display: block; }
body.is-exiting #loading-overlay, body.is-loading #loading-overlay { opacity: 1; }

#iris-in { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 0 500vmax var(--bg-color); z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); }
body.is-opening #iris-in { transform: translate(-50%, -50%) scale(500); transition: transform 1.2s cubic-bezier(0.85, 0, 0.15, 1); }
#iris-out { position: fixed; top: 50%; left: 50%; width: 150vmax; height: 150vmax; background-color: var(--bg-color); border-radius: 50%; z-index: 100001; pointer-events: none; transform: translate(-50%, -50%) scale(0); }
body.is-exiting #iris-out { transform: translate(-50%, -50%) scale(1.2); transition: transform 0.8s cubic-bezier(0.85, 0, 0.15, 1); }

body.is-loading > *:not([id^="iris-"]):not(#loading-overlay):not(#mode-toggle),
body.is-exiting > *:not([id^="iris-"]):not(#loading-overlay):not(#mode-toggle) { opacity: 0; }
body > *:not([id^="iris-"]):not(#loading-overlay):not(#mode-toggle) { transition: opacity 0.5s ease; }

.video-grid { display: grid !important; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)) !important; gap: 60px 40px !important; position: relative; }
.video-item { transition: all 0.4s ease; }
.video-item.sort-hide { opacity: 0; transform: scale(0.95); pointer-events: none; position: absolute; visibility: hidden; }
.video-thumbnail { width: 100%; aspect-ratio: 16/9; object-fit: cover; border-radius: 12px; }
.video-title { margin-top: 10px; font-size: 1rem; font-weight: 600; font-family: 'Noto Sans JP', sans-serif !important; }
.work-tag { font-size: 0.6rem; padding: 2px 6px; border: 0.5px solid var(--text-color); border-radius: 4px; margin-right: 4px; text-transform: uppercase; font-family: 'Montserrat', sans-serif !important; }
.filter-wrapper { margin-bottom: 40px; display: flex; flex-wrap: wrap; gap: 12px; }
#mode-toggle { cursor: pointer; background: none; border: 1px solid var(--text-color); color: var(--text-color); padding: 4px 12px; border-radius: 20px; position: fixed; top: 15px; right: 20px; z-index: 9999; font-weight: bold; }
</style>

<button id="mode-toggle">🌙 Dark Mode</button>

<script>
document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const html = document.documentElement;
  body.classList.add('is-loading');
  setTimeout(() => { body.classList.remove('is-loading'); body.classList.add('is-opening'); }, 100);

  const items = Array.from(document.querySelectorAll('.video-item'));
  const filterContainer = document.getElementById('filter-container');
  const allTags = new Set();
  items.forEach(item => item.dataset.tags.split(',').filter(t => t).forEach(t => allTags.add(t)));
  
  Array.from(allTags).sort().forEach(tag => {
    const btn = document.createElement('button');
    btn.className = 'filter-btn'; btn.textContent = tag;
    btn.style = "cursor:pointer; margin:4px; padding:6px 16px; border-radius:30px; border:1px solid var(--text-color); background:none; color:var(--text-color); opacity:0.3; font-family:'Montserrat',sans-serif; font-weight:700; text-transform:uppercase;";
    btn.onclick = () => {
      const isActive = btn.style.opacity === "1";
      btn.style.opacity = isActive ? "0.3" : "1";
      btn.style.background = isActive ? "none" : "var(--text-color)";
      btn.style.color = isActive ? "var(--text-color)" : "var(--bg-color)";
      
      const active = Array.from(filterContainer.querySelectorAll('button')).filter(b => b.style.opacity === "1").map(b => b.textContent);
      items.forEach(item => {
        const visible = active.length === 0 || active.some(f => item.dataset.tags.split(',').includes(f));
        item.classList.toggle('sort-hide', !visible);
        if(!visible) setTimeout(() => { if(item.classList.contains('sort-hide')) item.style.position = 'absolute'; }, 400);
        else { item.style.position = 'relative'; item.style.visibility = 'visible'; }
      });
    };
    filterContainer.appendChild(btn);
  });

  const toggle = document.getElementById('mode-toggle');
  if (localStorage.getItem('theme') === 'dark') { html.classList.add('dark-mode'); toggle.textContent = '☀️ Light Mode'; }
  toggle.addEventListener('click', () => {
    const isDark = html.classList.toggle('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    toggle.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
  });

  document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('#') || link.target === "_blank") return;
      e.preventDefault();
      body.classList.add('is-exiting');
      setTimeout(() => { window.location.href = href; }, 800);
    });
  });
});
</script>
"""
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    items = get_playlist_items()
    if items: update_markdown(items)
