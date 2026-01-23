import os
import json
import requests
import google.generativeai as genai
import html
import re

# --- 設定 ---
API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# プレイリストID
WORKS_PLAYLIST_ID = 'PLH9mX0wDlDAou_YCjcU01Q3pR6cCRQPWS'
RELEASE_PLAYLIST_ID = 'PLH9mX0wDlDAqZ8WMjS1uVJXpH3IiwTHGm'
MV_PLAYLIST_ID = 'PLH9mX0wDlDApen7-p7jxmAkDd1tWV9eeI'

# ファイルパス
CACHE_FILE = 'known_works.json'
MANUAL_WORKS_FILE = 'manual_works.json'
MANUAL_RELEASE_FILE = 'manual_release.json'
NEWS_FILE = 'news.json'
INDEX_FILE = 'index.md'

# マーカー定義
NEWS_START_MARKER = '<!-- NEWS_START -->'
NEWS_END_MARKER = '<!-- NEWS_END -->'

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, (list, dict)) else []
        except: return []
    return []

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

KNOWN_WORKS = load_json(CACHE_FILE)
if isinstance(KNOWN_WORKS, list): KNOWN_WORKS = {}

# Gemini設定
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        for m_name in ['gemini-2.0-flash', 'gemini-1.5-flash']:
            try:
                model = genai.GenerativeModel(model_name=m_name)
                break
            except: continue
    except: model = None

def get_tags(video_id, title, description, auto_tag=None):
    if auto_tag: return [auto_tag]
    if video_id in KNOWN_WORKS:
        cached = KNOWN_WORKS[video_id]
        if isinstance(cached, dict) and cached.get("tags"): return cached["tags"]
    tags = []
    if model:
        try:
            prompt = f"Identify Kakuly's role in '{title}' and output English tags only, comma separated. Desc: {description[:200]}"
            response = model.generate_content(prompt)
            result = response.text.strip()
            if result != "None": tags = [t.strip() for t in result.split(',')]
        except: pass
    if not tags:
        l_lower = (title + "\n" + description).lower()
        for pat, val in [('mix', 'Mix'), ('編曲', 'Arrangement'), ('master', 'Mastering'), ('movie', 'Movie'), ('music', 'Music'), ('作曲', 'Music'), ('lyric', 'Lyrics'), ('remix', 'Remix')]:
            if pat in l_lower: tags.append(val)
    
    normalized_tags = []
    for t in tags:
        t_clean = t.strip()
        if not t_clean: continue
        if t_clean.lower() in ['lyric', 'lyrics']: t_clean = 'Lyrics'
        elif t_clean.lower() == 'mv': t_clean = 'MV'
        elif t_clean.lower() == 'audio': t_clean = 'Audio'
        else: t_clean = t_clean.capitalize()
        normalized_tags.append(t_clean)
    
    processed = sorted(list(set(normalized_tags)))
    KNOWN_WORKS[video_id] = {"title": title, "tags": processed}
    save_json(CACHE_FILE, KNOWN_WORKS)
    return processed

def get_video_details(video_ids):
    details = {}
    if not API_KEY or not video_ids: return details
    for i in range(0, len(video_ids), 50):
        subset = ','.join(video_ids[i:i+50])
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={subset}&key={API_KEY}"
        try:
            r = requests.get(url, timeout=10).json()
            for item in r.get('items', []):
                details[item['id']] = {
                    "date": item['snippet']['publishedAt'][:10],
                    "channel": item['snippet']['channelTitle']
                }
        except: pass
    return details

def verify_thumbnail(video_id):
    for res in ['maxresdefault', 'hqdefault', 'mqdefault', 'default']:
        url = f'https://i.ytimg.com/vi/{video_id}/{res}.jpg'
        try:
            if requests.head(url, timeout=5).status_code == 200: return url
        except: continue
    return f'https://i.ytimg.com/vi/{video_id}/default.jpg'

def get_playlist_items(playlist_id):
    all_items = []
    if not API_KEY or not playlist_id or 'YOUR' in playlist_id: return []
    next_page_token = None
    while True:
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={API_KEY}"
        if next_page_token: url += f"&pageToken={next_page_token}"
        try:
            r = requests.get(url, timeout=10).json()
            items = r.get('items', [])
            all_items.extend(items)
            next_page_token = r.get('nextPageToken')
            if not next_page_token: break
        except: break
    return all_items

def process_items(items, auto_tag=None):
    video_ids = [item['snippet']['resourceId']['videoId'] for item in items]
    details = get_video_details(video_ids)
    processed = []
    for item in items:
        v_id = item['snippet']['resourceId']['videoId']
        info = details.get(v_id, {"date": item['snippet']['publishedAt'][:10], "channel": "Unknown"})
        processed.append({
            "title": html.escape(item['snippet']['title']),
            "video_id": v_id,
            "tags": get_tags(v_id, item['snippet']['title'], item['snippet']['description'], auto_tag),
            "date": info['date'],
            "artist": info['channel'],
            "thumbnail": verify_thumbnail(v_id),
            "type": "youtube",
            "size": "min"
        })
    return processed

def update_markdown():
    print(f"Fetching Works: {WORKS_PLAYLIST_ID}")
    works_yt = process_items(get_playlist_items(WORKS_PLAYLIST_ID))
    print(f"Fetching Release (Audio): {RELEASE_PLAYLIST_ID}")
    release_yt = process_items(get_playlist_items(RELEASE_PLAYLIST_ID), auto_tag="Audio")
    print(f"Fetching Release (MV): {MV_PLAYLIST_ID}")
    mv_yt = process_items(get_playlist_items(MV_PLAYLIST_ID), auto_tag="MV")
    
    def format_manual(data, default_artist="Kakuly"):
        formatted = []
        for d in data:
            formatted.append({
                "title": html.escape(d.get('title', 'Untitled')),
                "video_id": None,
                "tags": d.get('tags', []),
                "date": d.get('date', '2000-01-01'),
                "artist": d.get('artist', default_artist),
                "thumbnail": d.get('img') or d.get('image', ''),
                "url": d.get('url', '#'),
                "type": "manual",
                "size": d.get('size', 'min')
            })
        return formatted

    works_all = sorted(works_yt + format_manual(load_json(MANUAL_WORKS_FILE)), key=lambda x: x['date'], reverse=True)
    release_all = sorted(release_yt + mv_yt + format_manual(load_json(MANUAL_RELEASE_FILE)), key=lambda x: x['date'], reverse=True)

    pages = [
        {"file": "works.md", "title": "Works", "data": works_all, "permalink": "/works/", "show_artist": False},
        {"file": "release.md", "title": "Release", "data": release_all, "permalink": "/release/", "show_artist": True}
    ]

    for p in pages:
        content = generate_page_content(p['title'], p['data'], p['permalink'], p['show_artist'])
        with open(p['file'], 'w', encoding='utf-8') as f: f.write(content)

    update_index_with_news()

def update_index_with_news():
    news_data = load_json(NEWS_FILE)
    news_html = ''
    if news_data:
        news_data.sort(key=lambda x: x['date'], reverse=True)
        news_html = '\n<div class="news-section-wrapper">\n'
        news_html += '  <h2 class="section-title">NEWS</h2>\n'
        news_html += '  <div class="news-container-outer">\n'
        news_html += '    <button class="news-nav-btn prev" onclick="scrollNews(-1)" id="news-prev-btn">&#10094;</button>\n'
        news_html += '    <div class="news-scroll-container" id="news-scroll-container">\n'
        
        for item in news_data:
            content_for_modal = item["content"].replace('\n', '<br>')
            news_html += f'      <div class="news-card" onclick="openNewsModal(\'{item["id"]}\')">\n'
            news_html += f'        <div class="news-card-date">{item["date"]}</div>\n'
            news_html += f'        <div class="news-card-title">{item["title"]}</div>\n'
            news_html += f'        <div class="news-card-content-hidden" id="news-content-{item["id"]}" style="display:none;">{content_for_modal}</div>\n'
            news_html += '      </div>\n'
        
        news_html += '    </div>\n'
        news_html += '    <button class="news-nav-btn next" onclick="scrollNews(1)" id="news-next-btn">&#10095;</button>\n'
        news_html += '  </div>\n'
        news_html += '</div>\n'
        
        news_html += """
<div id="news-modal" class="modal">
  <div class="modal-content">
    <span class="close-modal" onclick="closeNewsModal()">&times;</span>
    <div id="modal-date" class="modal-date"></div>
    <h2 id="modal-title" class="modal-title"></h2>
    <div id="modal-body" class="modal-body"></div>
  </div>
</div>

<style>
.news-section-wrapper { margin: 40px 0; position: relative; z-index: 10; }
.news-section-wrapper .section-title { font-family: 'Montserrat', sans-serif; font-size: 1.8rem; margin-bottom: 20px; letter-spacing: -0.05em; }
.news-container-outer { position: relative; display: flex; align-items: center; }
.news-scroll-container { 
  display: flex; 
  overflow-x: auto; 
  gap: 20px; 
  padding: 20px 5px;
  scrollbar-width: none;
  -ms-overflow-style: none;
  scroll-behavior: smooth;
  width: 100%;
}
.news-scroll-container::-webkit-scrollbar { display: none; }

.news-card { 
  flex: 0 0 280px; 
  background: var(--bg-color); 
  border: 1px solid var(--text-color); 
  border-radius: 15px; 
  padding: 20px; 
  cursor: pointer; 
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  color: var(--text-color);
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.news-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
.news-card-date { font-family: 'Montserrat', sans-serif; font-size: 0.75rem; opacity: 0.7; margin-bottom: 8px; }
.news-card-title { font-size: 1rem; font-weight: 700; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }

.news-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: var(--bg-color);
  color: var(--text-color);
  border: 1px solid var(--text-color);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 11;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  opacity: 0;
  pointer-events: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.news-container-outer:hover .news-nav-btn.visible { opacity: 1; pointer-events: auto; }
.news-nav-btn.prev { left: -20px; }
.news-nav-btn.next { right: -20px; }
.news-nav-btn:hover { background: var(--text-color); color: var(--bg-color); }

.modal { display: none; position: fixed; z-index: 100001; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.8); backdrop-filter: blur(10px); }
.modal-content { background-color: var(--bg-color); margin: 10% auto; padding: 40px; border-radius: 20px; width: 85%; max-width: 600px; position: relative; color: var(--text-color); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
.close-modal { color: var(--text-color); float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
.modal-date { font-family: 'Montserrat', sans-serif; font-size: 0.9rem; opacity: 0.5; margin-bottom: 10px; }
.modal-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 20px; line-height: 1.3; }
.modal-body { font-size: 1rem; line-height: 1.8; }
</style>

<script>
function scrollNews(direction) {
  const container = document.getElementById('news-scroll-container');
  const scrollAmount = 600 * direction;
  container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
}

function updateNewsNav() {
  const container = document.getElementById('news-scroll-container');
  const prevBtn = document.getElementById('news-prev-btn');
  const nextBtn = document.getElementById('news-next-btn');
  if (!container || !prevBtn || !nextBtn) return;
  
  const isScrollable = container.scrollWidth > container.clientWidth;
  if (isScrollable) {
    prevBtn.classList.toggle('visible', container.scrollLeft > 10);
    nextBtn.classList.toggle('visible', container.scrollLeft < (container.scrollWidth - container.clientWidth - 10));
  } else {
    prevBtn.classList.remove('visible');
    nextBtn.classList.remove('visible');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('news-scroll-container');
  if (container) {
    container.addEventListener('scroll', updateNewsNav);
    window.addEventListener('resize', updateNewsNav);
    setTimeout(updateNewsNav, 500);
  }
});

function openNewsModal(id) {
  const contentElement = document.getElementById(`news-content-${id}`);
  const card = contentElement.closest('.news-card');
  const title = card.querySelector('.news-card-title').innerText;
  const date = card.querySelector('.news-card-date').innerText;
  const content = contentElement.innerHTML;
  document.getElementById('modal-title').innerText = title;
  document.getElementById('modal-date').innerText = date;
  document.getElementById('modal-body').innerHTML = content;
  document.getElementById('news-modal').style.display = "block";
  document.body.style.overflow = "hidden";
}
function closeNewsModal() {
  document.getElementById('news-modal').style.display = "none";
  document.body.style.overflow = "auto";
}
window.onclick = function(event) {
  if (event.target == document.getElementById('news-modal')) closeNewsModal();
}
</script>
"""
    if not os.path.exists(INDEX_FILE): return
    with open(INDEX_FILE, 'r', encoding='utf-8') as f: index_content = f.read()
    pattern = re.compile(f'{re.escape(NEWS_START_MARKER)}.*?{re.escape(NEWS_END_MARKER)}', re.DOTALL)
    if news_html:
        new_content = f'{NEWS_START_MARKER}\n{news_html}\n{NEWS_END_MARKER}'
        if pattern.search(index_content): updated_content = pattern.sub(new_content, index_content)
        else:
            if '## About' in index_content: updated_content = index_content.replace('## About', f'{new_content}\n\n## About')
            else: updated_content = index_content + "\n" + new_content
    else:
        new_content = f'{NEWS_START_MARKER}\n{NEWS_END_MARKER}'
        if pattern.search(index_content): updated_content = pattern.sub(new_content, index_content)
        else: updated_content = index_content
    with open(INDEX_FILE, 'w', encoding='utf-8') as f: f.write(updated_content)

def generate_page_content(title, works_data, permalink, show_artist):
    content = f"---\nlayout: page\ntitle: {title}\npermalink: {permalink}\n---\n\n"
    content += f"{title} - 作品集\n"
    content += '<div id="filter-container" class="filter-wrapper">\n'
    if show_artist: content += '  <div id="artist-filter" style="display:flex; flex-wrap:wrap; gap:12px; width:100%; margin-bottom:10px;"></div>\n'
    content += '  <div id="tag-filter" style="display:flex; flex-wrap:wrap; gap:12px; width:100%;"></div>\n'
    content += '</div>\n\n'
    content += '<div class="video-grid" id="video-grid">\n\n'
    for work in works_data:
        tags_attr = ",".join(work['tags'])
        size_class = f"size-{work['size']}"
        content += f'<div class="video-item {size_class}" data-tags="{tags_attr}" data-artist="{work["artist"]}">\n'
        if work['type'] == 'youtube':
            content += f'  <a href="https://www.youtube.com/watch?v={work["video_id"]}" target="_blank" class="video-link">\n'
            content += f'    <img src="{work["thumbnail"]}" data-video-id="{work["video_id"]}" data-error-attempt="0" alt="{work["title"]}" class="video-thumbnail" loading="lazy" onerror="handleImageError(this, \'{work["video_id"]}\')">\n'
            content += f'  </a>\n'
        else:
            content += f'  <a href="{work["url"]}" target="_blank" class="video-link">\n'
            content += f'    <img src="{work["thumbnail"]}" alt="{work["title"]}" class="video-thumbnail" loading="lazy">\n'
            content += f'  </a>\n'
        content += f"  <h3 class='video-title'>{work['title']}</h3>\n"
        if show_artist: content += f"  <p class='video-artist' style='font-size:0.75rem; font-weight:700; margin:4px 0 2px 0; opacity:0.8; font-family:\"Montserrat\", sans-serif;'>{work['artist']}</p>\n"
        content += f"  <p style='font-size:0.7rem; opacity:0.5; margin: 4px 0;'>{work['date']}</p>\n"
        if work['tags']:
            content += '  <div class="tag-container">\n'
            for tag in work['tags']: content += f'    <span class="work-tag">{tag}</span>\n'
            content += '  </div>\n'
        content += '</div>\n\n'
    content += '</div>\n\n<div id="iris-in"></div><div id="iris-out"></div>\n'
    content += """
<style>
.filter-wrapper { margin-bottom: 40px; display: flex; flex-wrap: wrap; gap: 12px; }
.filter-btn { cursor: pointer; font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; font-size: 0.9rem; padding: 6px 16px; border-radius: 30px; border: 1px solid var(--text-color); background: transparent; color: var(--text-color); transition: all 0.3s ease; text-transform: uppercase; opacity: 0.3; }
.filter-btn.active { opacity: 1; background: var(--text-color); color: var(--bg-color); }
.video-item { transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1), transform 0.4s cubic-bezier(0.4, 0, 0.2, 1); transform: scale(1); opacity: 1; }
.video-item.sort-hide { opacity: 0; transform: scale(0.95); pointer-events: none; position: absolute; visibility: hidden; }
.video-grid { grid-auto-flow: dense; }
.video-item.size-mid { grid-column: span 2; grid-row: span 2; }
.video-item.size-max { grid-column: span 3; grid-row: span 2; }
@media screen and (max-width: 900px) { .video-item.size-mid, .video-item.size-max { grid-column: span 1; grid-row: span 1; } }
.size-mid .video-thumbnail, .size-max .video-thumbnail { aspect-ratio: auto; height: auto; min-height: 200px; }
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
#mode-toggle { cursor: pointer; background: transparent; border: 1px solid var(--text-color); color: var(--text-color); padding: 6px 16px; border-radius: 20px; font-size: 0.75rem; position: fixed; top: 15px; right: 20px; z-index: 9999; font-weight: 700; font-family: 'Montserrat', sans-serif !important; transition: all 0.3s ease; backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
@media screen and (max-width: 1500px) { #mode-toggle { top: auto !important; bottom: 20px !important; right: 20px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.15); } }
#iris-in { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 0 500vmax var(--bg-color); z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 1.2s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-opening #iris-in { transform: translate(-50%, -50%) scale(500); }
#iris-out { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; background: var(--bg-color); z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 0.8s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-exiting #iris-out { transform: translate(-50%, -50%) scale(500) !important; }
body > *:not([id^="iris-"]) { opacity: 0; transition: opacity 0.8s ease-out; }
body.is-opening > *:not([id^="iris-"]) { opacity: 1; transition-delay: 0.2s; }
</style>
<button id="mode-toggle">🌙 Dark Mode</button>
<script>
function handleImageError(img, videoId) {
  const attempt = parseInt(img.getAttribute('data-error-attempt') || "0");
  if (attempt === 0) { img.setAttribute('data-error-attempt', "1"); img.src = 'https://i.ytimg.com/vi/' + videoId + '/hqdefault.jpg'; }
  else if (attempt === 1) { img.setAttribute('data-error-attempt', "2"); img.src = 'https://i.ytimg.com/vi/' + videoId + '/mqdefault.jpg'; }
}
document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('video-grid');
  const items = Array.from(grid.querySelectorAll('.video-item'));
  const artistFilter = document.getElementById('artist-filter');
  const tagFilter = document.getElementById('tag-filter');
  let activeArtist = 'ALL';
  let activeTags = new Set();
  const artists = new Set(['ALL']);
  const tags = new Set();
  items.forEach(item => {
    if (item.dataset.artist) {
      const firstArtist = item.dataset.artist.split(',')[0].trim();
      artists.add(firstArtist);
      item.setAttribute('data-filter-artist', firstArtist);
    }
    item.dataset.tags.split(',').filter(t => t).forEach(t => tags.add(t));
  });
  function createBtn(text, container, onClick, isAll=false) {
    const btn = document.createElement('button');
    btn.className = 'filter-btn' + (isAll ? ' active' : '');
    btn.textContent = text;
    btn.onclick = () => onClick(btn, text);
    container.appendChild(btn);
  }
  if (artistFilter) {
    Array.from(artists).sort().forEach(a => createBtn(a, artistFilter, (btn, val) => {
      artistFilter.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active'); activeArtist = val; apply();
    }, a === 'ALL'));
  }
  Array.from(tags).sort().forEach(t => createBtn(t, tagFilter, (btn, val) => {
    btn.classList.toggle('active');
    if (activeTags.has(val)) activeTags.delete(val); else activeTags.add(val);
    apply();
  }));
  function apply() {
    items.forEach(item => {
      const aMatch = activeArtist === 'ALL' || item.getAttribute('data-filter-artist') === activeArtist;
      const tMatch = activeTags.size === 0 || Array.from(activeTags).every(t => item.dataset.tags.split(',').includes(t));
      if (aMatch && tMatch) { item.classList.remove('sort-hide'); item.style.position = 'relative'; item.style.visibility = 'visible'; item.style.pointerEvents = 'auto'; }
      else { item.classList.add('sort-hide'); setTimeout(() => { if (item.classList.contains('sort-hide')) { item.style.position = 'absolute'; } }, 400); }
    });
  }
});
const btn = document.getElementById('mode-toggle');
const body = document.body;
const html = document.documentElement;
if (localStorage.getItem('theme') === 'dark') { html.classList.add('dark-mode'); body.classList.add('dark-mode'); btn.textContent = '☀️ Light Mode'; }
btn.addEventListener('click', () => {
  body.classList.add('mode-transition');
  const isDark = html.classList.toggle('dark-mode');
  body.classList.toggle('dark-mode');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
  setTimeout(() => { body.classList.remove('mode-transition'); }, 500);
});
function startIris() { document.body.classList.remove('is-opening', 'is-exiting'); requestAnimationFrame(() => { setTimeout(() => { document.body.classList.add('is-opening'); }, 50); }); }
window.addEventListener('pageshow', startIris);
document.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', (e) => {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.includes('mailto:') || link.target === "_blank") return;
    e.preventDefault(); document.body.classList.add('is-exiting');
    setTimeout(() => { window.location.href = href; }, 700);
  });
});
</script>
"""
    return content

if __name__ == "__main__":
    update_markdown()
