import os
import requests

# 設定
API_KEY = os.environ['YOUTUBE_API_KEY']
PLAYLIST_ID = 'PLH9mX0wDlDAowW9zPkyOygWJXXzLcHDRN'
FILE_PATH = 'works.md'

def get_playlist_items():
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=10&playlistId={PLAYLIST_ID}&key={API_KEY}"
    response = requests.get(url).json()
    items = response.get('items', [])
    return items

def update_markdown(items):
    content = "---\nlayout: page\ntitle: Works\npermalink: /works/\n---\n\n## YouTube Playlist (Auto Updated)\n\n"
    
    for item in items:
        title = item['snippet']['title']
        video_id = item['snippet']['resourceId']['videoId']
        url = f"https://www.youtube.com/watch?v={video_id}"
        thumbnail = item['snippet']['thumbnails']['medium']['url']
        
        content += f"### {title}\n"
        content += f"[![Thumbnail]({thumbnail})]({url})\n\n"
        content += f"[動画を見る]({url})\n\n---\n\n"
        
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    items = get_playlist_items()
    if items:
        update_markdown(items)
        print("Successfully updated works.md")
