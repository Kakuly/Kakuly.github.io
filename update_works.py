import os
import json
import requests
import google.generativeai as genai
import html
from datetime import datetime

# --- 設定 ---
API_KEY = os.environ['YOUTUBE_API_KEY']
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
PLAYLIST_ID = 'PLH9mX0wDlDAou_YCjcU01Q3pR6cCRQPWS'
FILE_PATH = 'works.md'
CACHE_FILE = 'known_works.json'
MANUAL_FILE = 'manual_works.json'

def load_json_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return [] if "manual" in file_path else {}
    return [] if "manual" in file_path else {}

def save_known_works(data):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

KNOWN_WORKS = load_json_data(CACHE_FILE)
MANUAL_WORKS = load_json_data(MANUAL_FILE)

def get_video_details(video_ids):
    """動画の投稿日を取得"""
    details = {}
    for i in range(0, len(video_ids), 50):
        ids_subset = ','.join(video_ids[i:i+50])
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ids_subset}&key={API_KEY}"
        try:
            r = requests.get(url).json()
            for item in r.get('items', []):
                details[item['id']] = item['snippet']['publishedAt'][:10]
        except: pass
    return details

def update_markdown():
    # 1. YouTubeデータの取得
    items = []
    next_page_token = None
    while True:
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={PLAYLIST_ID}&key={API_KEY}"
        if next_page_token: url += f"&pageToken={next_page_token}"
        r = requests.get(url).json()
        items.extend(r.get('items', []))
        next_page_token = r.get('nextPageToken')
        if not next_page_token: break

    video_ids = [it['snippet']['resourceId']['videoId'] for it in items]
    actual_dates = get_video_details(video_ids)

    all_works = []
    for it in items:
        snippet = it['snippet']
        v_id = snippet['resourceId']['videoId']
        actual_date = actual_dates.get(v_id, snippet['publishedAt'][:10])
        
        # キャッシュ確認
        cached = KNOWN_WORKS.get(v_id, {})
        date = cached.get("date", actual_date)
        tags = cached.get("tags", [])
        
        # サムネイル
        img_url = ""
        thumbs = snippet.get('thumbnails', {})
        for res in ['maxres', 'standard', 'high', 'medium', 'default']:
            if res in thumbs:
                img_url = thumbs[res]['url']
                break

        all_works.append({
            "title": html.escape(snippet['title']),
            "date": date,
            "img": img_url,
            "url": f"https://www.youtube.com/watch?v={v_id}",
            "tags": tags
        })
        
        # キャッシュ保存
        KNOWN_WORKS[v_id] = {"title": snippet['title'], "tags": tags, "date": date}

    save_known_works(KNOWN_WORKS)

    # 2. 手動データの合流とソート
    all_works.extend(MANUAL_WORKS)
    all_works.sort(key=lambda x: x['date'], reverse=True)

    # 3. ファイル書き出し
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        # ヘッダー (体系を厳守)
        f.write("---\n")
        f.write("layout: page\n")
        f.write("title: Works\n")
        f.write("permalink: /works/\n")
        f.write("---\n\n")
        f.write("関わった／制作した作品集\n\n")
        f.write('<div id="filter-container" class="filter-wrapper"></div>\n\n')
        f.write('<div class="video-grid" id="video-grid">\n\n')
        
        for work in all_works:
            tags_attr = ",".join(work['tags'])
            f.write(f'<div class="video-item" data-tags="{tags_attr}">\n')
            f.write(f'  <a href="{work["url"]}" target="_blank" class="video-link">\n')
            f.write(f'    <img src="{work["img"]}" alt="{work["title"]}" class="video-thumbnail" loading="lazy">\n')
            f.write(f'  </a>\n')
            f.write(f"  <h3 class='video-title'>{work['title']}</h3>\n")
            f.write(f"  <p style='font-size:0.7rem; opacity:0.5; margin: 4px 0;'>{work['date']}</p>\n")
            if work['tags']:
                f.write('  <div class="tag-container">\n')
                for tag in work['tags']:
                    f.write(f'    <span class="work-tag">{tag}</span>\n')
                f.write('  </div>\n')
            f.write('</div>\n\n')

        f.write('</div>\n\n<div id="iris-in"></div><div id="iris-out"></div>\n')
        
        # スタイルとスクリプト (改行を以前の形に完全固定)
        f.write("""
<style>
.filter-wrapper { margin-bottom: 40px; display: flex; flex-wrap: wrap; gap: 12px; }
.filter-btn { cursor: pointer; font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; font-size: 0.9rem; padding: 6px 16px; border-radius: 30px; border: 1px solid var(--text-color); background: transparent; color: var(--text-color); transition: all 0.3s ease; text-transform: uppercase; opacity: 0.3; }
.filter-btn.active { opacity: 1; background: var(--text-color); color: var(--bg-color); }
.video-item { transition: opacity 0.4s ease, transform 0.4s ease; transform: scale(1); opacity: 1; }
.video-item.sort-hide { opacity: 0; transform: scale(0.95); pointer-events: none; position: absolute; visibility: hidden; }
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
.video-grid { display: grid !important; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)) !important; gap: 60px 40px !important; position: relative; }
#mode-toggle { cursor: pointer; background: transparent; border: 1px solid var(--text-color); color: var(--text-color); padding: 6px 16px; border-radius: 20px; font-size: 0.75rem; position: fixed; top: 15px; right: 20px; z-index: 9999; font-weight: 700; font-family: 'Montserrat', sans-serif !important; backdrop-filter: blur(8px); }
@media screen and (max-width: 1500px) { #mode-toggle { top: auto !important; bottom: 20px !important; right: 20px !important; } }
#iris-in { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 0 500vmax var(--bg-color); z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 1.2s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-opening #iris-in { transform: translate(-50%, -50%) scale(500); }
#iris-out { position: fixed; top: 50%; left: 50%; width: 150vmax; height: 150vmax; background-color: var(--bg-color); border-radius: 50%; z-index: 100001; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 0.8s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-exiting #iris-out { transform: translate(-50%, -50%) scale(1.2) !important; }
body > *:not([id^="iris-"]) { opacity: 0; transition: opacity 0.8s ease-out; }
body.is-opening > *:not([id^="iris-"]) { opacity: 1; }
</style>
<button id="mode-toggle">🌙 Dark Mode</button>
<script>
  document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('video-grid');
    const items = Array.from(grid.querySelectorAll('.video-item'));
    const filterContainer = document.getElementById('filter-container');
    const activeFilters = new Set();
    const allTags = new Set();
    items.forEach(item => { item.dataset.tags.split(',').filter(t => t).forEach(t => allTags.add(t)); });
    Array.from(allTags).sort().forEach(tag => {
      const btn = document.createElement('button');
      btn.className = 'filter-btn';
      btn.textContent = tag;
      btn.onclick = () => {
        btn.classList.toggle('active');
        if (activeFilters.has(tag)) activeFilters.delete(tag);
        else activeFilters.add(tag);
        items.forEach(it => {
          const itTags = it.dataset.tags.split(',');
          const visible = activeFilters.size === 0 || Array.from(activeFilters).every(f => itTags.includes(f));
          it.classList.toggle('sort-hide', !visible);
          it.style.position = visible ? 'relative' : 'absolute';
        });
      };
      filterContainer.appendChild(btn);
    });
  });
  const btn = document.getElementById('mode-toggle');
  const html = document.documentElement;
  if (localStorage.getItem('theme') === 'dark') { html.classList.add('dark-mode'); document.body.classList.add('dark-mode'); btn.textContent = '☀️ Light Mode'; }
  btn.addEventListener('click', () => {
    const isDark = html.classList.toggle('dark-mode');
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
  });
  window.addEventListener('pageshow', () => { setTimeout(() => document.body.classList.add('is-opening'), 50); });
</script>
""")

if __name__ == "__main__":
    update_markdown()
