import os
import json
import requests
import google.generativeai as genai
import html

# --- 設定 ---
API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# プレイリストID
WORKS_PLAYLIST_ID = 'PLH9mX0wDlDAou_YCjcU01Q3pR6cCRQPWS'
RELEASE_PLAYLIST_ID = 'PLH9mX0wDlDApS_YOUR_RELEASE_PLAYLIST_ID' # ここにRelease用のプレイリストIDを設定してください

# ファイルパス
CACHE_FILE = 'known_works.json'
MANUAL_WORKS_FILE = 'manual_works.json'
MANUAL_RELEASE_FILE = 'manual_release.json'

# --- JSON読み込み ---
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
if isinstance(KNOWN_WORKS, list): KNOWN_WORKS = {} # 互換性維持

# Gemini設定
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

def get_tags(video_id, title, description, is_release=False):
    if is_release: return ["MV"] # Releaseは固定でMV
    
    if video_id in KNOWN_WORKS:
        cached = KNOWN_WORKS[video_id]
        if isinstance(cached, dict) and cached.get("tags"): return cached["tags"]

    tags = []
    if model:
        try:
            prompt = f"楽曲クレジット専門家として、動画「{title}」でのKakulyの担当役割を特定し、英語タグのみカンマ区切りで出力してください。概要: {description[:300]}"
            response = model.generate_content(prompt)
            result = response.text.strip()
            if result != "None": tags = [t.strip() for t in result.split(',')]
        except: pass

    if not tags:
        l_lower = (title + "\n" + description).lower()
        for pat, val in [('mix', 'Mix'), ('編曲', 'Arrangement'), ('master', 'Mastering'), ('movie', 'Movie'), ('music', 'Music'), ('作曲', 'Music'), ('lyric', 'Lyrics'), ('remix', 'Remix')]:
            if pat in l_lower: tags.append(val)
    
    processed = sorted(list(set([t.replace('Lyric', 'Lyrics') if t == 'Lyric' else t for t in tags])))
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

def process_items(items, is_release=False):
    video_ids = [item['snippet']['resourceId']['videoId'] for item in items]
    details = get_video_details(video_ids)
    processed = []
    for item in items:
        v_id = item['snippet']['resourceId']['videoId']
        info = details.get(v_id, {"date": item['snippet']['publishedAt'][:10], "channel": "Unknown"})
        processed.append({
            "title": html.escape(item['snippet']['title']),
            "video_id": v_id,
            "tags": get_tags(v_id, item['snippet']['title'], item['snippet']['description'], is_release),
            "date": info['date'],
            "artist": info['channel'], # YouTubeはチャンネル名をデフォルトアーティストに
            "thumbnail": verify_thumbnail(v_id),
            "type": "youtube",
            "size": "min"
        })
    return processed

def update_markdown():
    # データ取得
    works_yt = process_items(get_playlist_items(WORKS_PLAYLIST_ID), is_release=False)
    release_yt = process_items(get_playlist_items(RELEASE_PLAYLIST_ID), is_release=True)
    
    works_manual = load_json(MANUAL_WORKS_FILE)
    release_manual = load_json(MANUAL_RELEASE_FILE)
    
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

    works_all = sorted(works_yt + format_manual(works_manual), key=lambda x: x['date'], reverse=True)
    release_all = sorted(release_yt + format_manual(release_manual), key=lambda x: x['date'], reverse=True)

    pages = [
        {"file": "works.md", "title": "Works", "data": works_all, "permalink": "/works/"},
        {"file": "release.md", "title": "Release", "data": release_all, "permalink": "/release/"}
    ]

    for p in pages:
        content = generate_page_content(p['title'], p['data'], p['permalink'])
        with open(p['file'], 'w', encoding='utf-8') as f: f.write(content)
        print(f"Generated: {p['file']} ({len(p['data'])} items)")

def generate_page_content(title, works_data, permalink):
    content = f"---\nlayout: page\ntitle: {title}\npermalink: {permalink}\n---\n\n"
    content += f"{title} - 作品集\n\n"
    
    # フィルタUI
    content += '<div class="filter-section">\n'
    content += '  <div class="filter-label">Artist:</div>\n'
    content += '  <div id="artist-filter" class="filter-wrapper"></div>\n'
    content += '  <div class="filter-label">Tags:</div>\n'
    content += '  <div id="tag-filter" class="filter-wrapper"></div>\n'
    content += '</div>\n\n'
    
    content += '<div class="video-grid" id="video-grid">\n\n'
    for work in works_data:
        tags_attr = ",".join(work['tags'])
        content += f'<div class="video-item size-{work["size"]}" data-tags="{tags_attr}" data-artist="{work["artist"]}">\n'
        if work['type'] == 'youtube':
            content += f'  <a href="https://www.youtube.com/watch?v={work["video_id"]}" target="_blank" class="video-link">\n'
            content += f'    <img src="{work["thumbnail"]}" data-video-id="{work["video_id"]}" data-error-attempt="0" alt="{work["title"]}" class="video-thumbnail" loading="lazy" onerror="handleImageError(this)">\n'
            content += f'  </a>\n'
        else:
            content += f'  <a href="{work["url"]}" target="_blank" class="video-link">\n'
            content += f'    <img src="{work["thumbnail"]}" alt="{work["title"]}" class="video-thumbnail" loading="lazy">\n'
            content += f'  </a>\n'
        content += f"  <h3 class='video-title'>{work['title']}</h3>\n"
        content += f"  <p class='video-artist'>{work['artist']}</p>\n"
        content += f"  <p class='video-date'>{work['date']}</p>\n"
        if work['tags']:
            content += '  <div class="tag-container">' + "".join([f'<span class="work-tag">{t}</span>' for t in work['tags']]) + '</div>\n'
        content += '</div>\n\n'
    content += '</div>\n<div id="iris-in"></div><div id="iris-out"></div>\n'

    content += """
<style>
.filter-section { margin-bottom: 40px; }
.filter-label { font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 0.7rem; text-transform: uppercase; opacity: 0.5; margin-bottom: 8px; margin-top: 15px; }
.filter-wrapper { display: flex; flex-wrap: wrap; gap: 10px; }
.filter-btn { cursor: pointer; font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; font-size: 0.8rem; padding: 5px 14px; border-radius: 20px; border: 1px solid var(--text-color); background: transparent; color: var(--text-color); transition: all 0.3s ease; text-transform: uppercase; opacity: 0.3; }
.filter-btn.active { opacity: 1; background: var(--text-color); color: var(--bg-color); }
.video-grid { display: grid !important; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)) !important; gap: 60px 40px !important; grid-auto-flow: dense; }
.video-item { transition: opacity 0.4s ease, transform 0.4s ease; backface-visibility: hidden; }
.video-item.size-mid { grid-column: span 2; grid-row: span 2; }
.video-item.size-max { grid-column: span 3; grid-row: span 2; }
@media screen and (max-width: 900px) { .video-item.size-mid, .video-item.size-max { grid-column: span 1; grid-row: span 1; } }
.video-item.sort-hide { opacity: 0; transform: scale(0.95); pointer-events: none; }
.video-thumbnail { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 12px; transition: transform 0.3s ease; }
.size-mid .video-thumbnail, .size-max .video-thumbnail { aspect-ratio: auto; height: auto; min-height: 200px; }
.video-title { margin-top: 10px; font-size: 0.95rem; font-weight: 700; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; font-family: 'Noto Sans JP', sans-serif !important; }
.video-artist { font-size: 0.75rem; font-weight: 700; margin: 4px 0 2px 0; opacity: 0.8; font-family: 'Montserrat', sans-serif; }
.video-date { font-size: 0.65rem; opacity: 0.5; margin: 0; }
.tag-container { margin-top: 8px; display: flex; flex-wrap: wrap; gap: 5px; }
.work-tag { font-size: 0.55rem; padding: 1px 6px; border-radius: 4px; border: 0.5px solid var(--text-color); opacity: 0.7; font-family: 'Montserrat', sans-serif; text-transform: uppercase; }
.wrapper { max-width: 1100px !important; }
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Noto+Sans+JP:wght@400;700&display=swap');
:root { --bg-color: #ffffff; --text-color: #111111; }
html.dark-mode, body.dark-mode { --bg-color: #000000; --text-color: #eeeeee; background-color: #000000 !important; }
body { background-color: var(--bg-color) !important; color: var(--text-color) !important; font-family: 'Noto Sans JP', sans-serif !important; font-weight: 700 !important; }
#mode-toggle { cursor: pointer; background: transparent; border: 1px solid var(--text-color); color: var(--text-color); padding: 6px 16px; border-radius: 20px; font-size: 0.75rem; position: fixed; top: 15px; right: 20px; z-index: 9999; font-weight: 700; font-family: 'Montserrat', sans-serif !important; }
#iris-in, #iris-out { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 1s ease; }
#iris-in { box-shadow: 0 0 0 500vmax var(--bg-color); }
#iris-out { background: var(--bg-color); }
body.is-opening #iris-in { transform: translate(-50%, -50%) scale(500); }
body.is-exiting #iris-out { transform: translate(-50%, -50%) scale(1.2); }
</style>
<button id="mode-toggle">🌙 Dark Mode</button>
<script>
function handleImageError(img) {
  const vId = img.dataset.videoId; if (!vId) return;
  const attempt = parseInt(img.dataset.errorAttempt || "0");
  const urls = [`https://i.ytimg.com/vi/${vId}/hqdefault.jpg`,`https://i.ytimg.com/vi/${vId}/mqdefault.jpg`,`https://i.ytimg.com/vi/${vId}/default.jpg`];
  if (attempt < urls.length) { img.dataset.errorAttempt = attempt + 1; img.src = urls[attempt]; }
}
document.addEventListener('DOMContentLoaded', () => {
  const items = Array.from(document.querySelectorAll('.video-item'));
  const artistFilter = document.getElementById('artist-filter');
  const tagFilter = document.getElementById('tag-filter');
  let activeArtist = 'ALL';
  let activeTags = new Set();

  const artists = new Set(['ALL']);
  const tags = new Set();
  items.forEach(item => {
    artists.add(item.dataset.artist);
    item.dataset.tags.split(',').filter(t => t).forEach(t => tags.add(t));
  });

  function createBtn(text, container, onClick, isAll=False) {
    const btn = document.createElement('button');
    btn.className = 'filter-btn' + (isAll ? ' active' : '');
    btn.textContent = text;
    btn.onclick = () => onClick(btn, text);
    container.appendChild(btn);
  }

  Array.from(artists).sort().forEach(a => createBtn(a, artistFilter, (btn, val) => {
    artistFilter.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active'); activeArtist = val; apply();
  }, a === 'ALL'));

  Array.from(tags).sort().forEach(t => createBtn(t, tagFilter, (btn, val) => {
    btn.classList.toggle('active');
    if (activeTags.has(val)) activeTags.delete(val); else activeTags.add(val);
    apply();
  }));

  function apply() {
    items.forEach(item => {
      const aMatch = activeArtist === 'ALL' || item.dataset.artist === activeArtist;
      const tMatch = activeTags.size === 0 || Array.from(activeTags).every(t => item.dataset.tags.split(',').includes(t));
      if (aMatch && tMatch) {
        item.classList.remove('sort-hide'); item.style.display = ''; item.style.position = 'relative';
      } else {
        item.classList.add('sort-hide'); setTimeout(() => { if (item.classList.contains('sort-hide')) { item.style.display = 'none'; item.style.position = 'absolute'; } }, 400);
      }
    });
  }
});
const btn = document.getElementById('mode-toggle');
if (localStorage.getItem('theme') === 'dark') { document.documentElement.classList.add('dark-mode'); btn.textContent = '☀️ Light Mode'; }
btn.onclick = () => {
  const isDark = document.documentElement.classList.toggle('dark-mode');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
};
window.addEventListener('pageshow', () => { document.body.classList.add('is-opening'); });
document.querySelectorAll('a').forEach(link => {
  link.onclick = (e) => {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || link.target === "_blank") return;
    e.preventDefault(); document.body.classList.add('is-exiting');
    setTimeout(() => { window.location.href = href; }, 800);
  };
});
</script>
"""
    return content

if __name__ == "__main__":
    update_markdown()
