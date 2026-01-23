import os
import json
import requests
import google.generativeai as genai
import html

# --- 設定 ---
API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
PLAYLIST_ID = 'PLH9mX0wDlDAou_YCjcU01Q3pR6cCRQPWS'
FILE_PATH = 'works.md'
CACHE_FILE = 'known_works.json'
MANUAL_WORKS_FILE = 'manual_works.json'

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

def load_manual_works():
    """manual_works.jsonから手動作品を読み込む"""
    if os.path.exists(MANUAL_WORKS_FILE):
        try:
            with open(MANUAL_WORKS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            print(f"Error loading manual_works.json: {e}")
            return []
    return []

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
        
        【参考:Kakulyの過去の実績傾向】
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

def get_video_published_dates(video_ids):
    """動画本来の投稿日を一括取得するための追加関数"""
    dates = {}
    if not API_KEY: return dates
    for i in range(0, len(video_ids), 50):
        subset = ','.join(video_ids[i:i+50])
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={subset}&key={API_KEY}"
        try:
            r = requests.get(url, timeout=10).json()
            for item in r.get('items', []):
                dates[item['id']] = item['snippet']['publishedAt'][:10]
        except: pass
    return dates

def verify_thumbnail(video_id):
    """サムネイルが存在するか確認し、最適なURLを返す"""
    thumbnail_urls = [
        f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg',
        f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg',
        f'https://i.ytimg.com/vi/{video_id}/mqdefault.jpg',
        f'https://i.ytimg.com/vi/{video_id}/default.jpg'
    ]
    
    for url in thumbnail_urls:
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                return url
        except:
            continue
    
    # すべて失敗した場合はデフォルトを返す
    return thumbnail_urls[-1]

def get_playlist_items():
    all_items = []
    if not API_KEY:
        print("Warning: YOUTUBE_API_KEY is not set.")
        return []
    next_page_token = None
    while True:
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={PLAYLIST_ID}&key={API_KEY}"
        if next_page_token: url += f"&pageToken={next_page_token}"
        try:
            r = requests.get(url, timeout=10).json()
            items = r.get('items', [])
            all_items.extend(items)
            next_page_token = r.get('nextPageToken')
            if not next_page_token: break
        except Exception as e:
            print(f"Error fetching playlist: {e}")
            break
    return all_items

def update_markdown(items):
    # 動画IDのリストを作成して投稿日を一括取得
    video_ids = [item['snippet']['resourceId']['videoId'] for item in items]
    actual_dates = get_video_published_dates(video_ids)

    # YouTubeから取得したデータを整理
    works_data = []
    for item in items:
        snippet = item['snippet']
        v_id = snippet['resourceId']['videoId']
        # 公開日を取得（取得できなければフォールバック）
        pub_date = actual_dates.get(v_id, snippet['publishedAt'][:10])
        tags = get_tags(v_id, snippet['title'], snippet['description'])
        
        # サムネイルURLを事前に検証
        thumbnail_url = verify_thumbnail(v_id)
        
        works_data.append({
            "title": html.escape(snippet['title']),
            "video_id": v_id,
            "tags": tags,
            "date": pub_date,
            "thumbnail": thumbnail_url,
            "type": "youtube"
        })
    
    # manual_works.jsonから手動作品を読み込んで追加
    manual_works = load_manual_works()
    for manual_work in manual_works:
        thumbnail = manual_work.get('img') or manual_work.get('image', '')
        works_data.append({
            "title": html.escape(manual_work.get('title', 'Untitled')),
            "video_id": None,
            "tags": manual_work.get('tags', []),
            "date": manual_work.get('date', '2000-01-01'),
            "thumbnail": thumbnail,
            "url": manual_work.get('url', '#'),
            "type": "manual"
        })
    
    # 投稿日の降順でソート
    works_data.sort(key=lambda x: x['date'], reverse=True)

    # ページネーション設定 (1ページ51個)
    items_per_page = 51
    total_items = len(works_data)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    print(f"Total items: {total_items}, Total pages: {total_pages}")

    # ページごとにファイルを生成
    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        page_works = works_data[start_idx:end_idx]
        
        # ファイル名の決定
        if page_num == 1:
            file_path = FILE_PATH
        else:
            file_path = f'works_page{page_num}.md'
        
        content = generate_page_content(page_works, page_num, total_pages)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Generated: {file_path} (Items {start_idx+1} to {end_idx})")
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
    
    print(f"生成完了: {total_pages}ページ、合計{total_items}作品")

def generate_page_content(works_data, current_page, total_pages):
    """ページコンテンツを生成"""
    # タイトルから「- Page X」を削除し、常に「Works」にする
    content = "---\nlayout: page\ntitle: Works"
    
    if current_page == 1:
        content += "\npermalink: /works/"
    else:
        content += f"\npermalink: /works/page{current_page}/"
    content += "\n---\n\n"
    
    content += "関わった／制作した作品集\n"
    
    # ページネーションナビゲーション
    if total_pages > 1:
        content += '<div class="pagination-nav">\n'
        if current_page > 1:
            prev_link = '/works/' if current_page == 2 else f'/works/page{current_page-1}/'
            content += f'  <a href="{prev_link}" class="pagination-btn">← 前のページ</a>\n'
        content += f'  <span class="pagination-info">Page {current_page} / {total_pages}</span>\n'
        if current_page < total_pages:
            content += f'  <a href="/works/page{current_page+1}/" class="pagination-btn">次のページ →</a>\n'
        content += '</div>\n\n'
    
    content += '<div id="filter-container" class="filter-wrapper"></div>\n\n'
    content += '<div class="video-grid" id="video-grid">\n\n'
    
    for work in works_data:
        tags_attr = ",".join(work['tags']) if work['tags'] else ""
        
        content += f'<div class="video-item" data-tags="{tags_attr}">\n'
        
        if work['type'] == 'youtube':
            content += f'  <a href="https://www.youtube.com/watch?v={work["video_id"]}" target="_blank" class="video-link">\n'
            content += f'    <img src="{work["thumbnail"]}" '
            content += f'data-video-id="{work["video_id"]}" '
            content += f'data-error-attempt="0" '
            content += f'alt="{work["title"]}" class="video-thumbnail" loading="lazy" '
            content += f'onerror="handleImageError(this)">\n'
            content += f'  </a>\n'
        else:
            content += f'  <a href="{work["url"]}" target="_blank" class="video-link">\n'
            content += f'    <img src="{work["thumbnail"]}" '
            content += f'alt="{work["title"]}" class="video-thumbnail" loading="lazy">\n'
            content += f'  </a>\n'
        
        content += f"  <h3 class='video-title'>{work['title']}</h3>"
        content += f"\n  <p style='font-size:0.7rem; opacity:0.5; margin: 4px 0;'>{work['date']}</p>"
        
        if work['tags']:
            content += '\n  <div class="tag-container">\n'
            for tag in work['tags']:
                content += f'    <span class="work-tag">{tag}</span>\n'
            content += '  </div>\n'
        content += '</div>\n\n'

    content += '</div>\n\n'
    
    if total_pages > 1:
        content += '<div class="pagination-nav pagination-bottom">\n'
        if current_page > 1:
            prev_link = '/works/' if current_page == 2 else f'/works/page{current_page-1}/'
            content += f'  <a href="{prev_link}" class="pagination-btn">← 前のページ</a>\n'
        content += f'  <span class="pagination-info">Page {current_page} / {total_pages}</span>\n'
        if current_page < total_pages:
            content += f'  <a href="/works/page{current_page+1}/" class="pagination-btn">次のページ →</a>\n'
        content += '</div>\n\n'

    content += '<div id="iris-in"></div>'
    content += '<div id="iris-out"></div>'

    content += """
<style>
/* --- ページネーション --- */
.pagination-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin: 30px 0;
  flex-wrap: wrap;
}
.pagination-bottom {
  margin-top: 60px;
}
.pagination-btn {
  font-family: 'Montserrat', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.9rem;
  padding: 10px 20px;
  border-radius: 30px;
  border: 1px solid var(--text-color);
  background: transparent;
  color: var(--text-color);
  text-decoration: none;
  transition: all 0.3s ease;
  text-transform: uppercase;
}
.pagination-btn:hover {
  background: var(--text-color);
  color: var(--bg-color);
}
.pagination-info {
  font-family: 'Montserrat', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.9rem;
  opacity: 0.7;
}

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
  backface-visibility: hidden;
}
.video-item.sort-hide {
  opacity: 0;
  transform: scale(0.95);
  pointer-events: none;
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

#mode-toggle { 
    cursor: pointer; 
    background: transparent; 
    border: 1px solid var(--text-color); 
    color: var(--text-color); 
    padding: 6px 16px; 
    border-radius: 20px; 
    font-size: 0.75rem; 
    position: fixed; 
    top: 15px; 
    right: 20px; 
    z-index: 9999; 
    font-weight: 700;
    font-family: 'Montserrat', sans-serif !important; 
    transition: all 0.3s ease;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

@media screen and (max-width: 1500px) {
    #mode-toggle {
        top: auto !important;
        bottom: 20px !important;
        right: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15); 
    }
}

#iris-in { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 0 500vmax var(--bg-color); z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 1.2s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-opening #iris-in { transform: translate(-50%, -50%) scale(500); }
#iris-out { position: fixed; top: 50%; left: 50%; width: 10px; height: 10px; border-radius: 50%; background: var(--bg-color); z-index: 100000; pointer-events: none; transform: translate(-50%, -50%) scale(0); transition: transform 0.8s cubic-bezier(0.85, 0, 0.15, 1); }
body.is-exiting #iris-out { transform: translate(-50%, -50%) scale(1.2) !important; }
body > *:not([id^="iris-"]) { opacity: 0; transition: opacity 0.8s ease-out; }
body.is-opening > *:not([id^="iris-"]) { opacity: 1; transition-delay: 0.2s; }
</style>

<button id="mode-toggle">🌙 Dark Mode</button>

<script>

function handleImageError(img) {
  const videoId = img.getAttribute('data-video-id');
  if (!videoId) return; 
  
  const attempt = parseInt(img.getAttribute('data-error-attempt') || "0");
  const fallbackUrls = [
    'https://i.ytimg.com/vi/' + videoId + '/hqdefault.jpg',
    'https://i.ytimg.com/vi/' + videoId + '/mqdefault.jpg',
    'https://i.ytimg.com/vi/' + videoId + '/default.jpg'
  ];
  
  if (attempt < fallbackUrls.length) {
    img.setAttribute('data-error-attempt', (attempt + 1).toString());
    img.src = fallbackUrls[attempt];
  } else {
    img.style.backgroundColor = '#333';
    img.alt = '画像を読み込めませんでした';
  }
}

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
        const isVisible = activeFilters.size === 0 || Array.from(activeFilters).every(f => itemTags.includes(f));
        
        if (isVisible) {
          item.classList.remove('sort-hide');
          item.style.display = ''; 
          item.style.position = 'relative';
          item.style.pointerEvents = 'auto';
          item.style.visibility = 'visible';
        } else {
          item.classList.add('sort-hide');
          item.style.pointerEvents = 'none';
          setTimeout(() => {
            if (item.classList.contains('sort-hide')) {
              item.style.display = 'none';
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

    return content

if __name__ == "__main__":
    items = get_playlist_items()
    update_markdown(items)
