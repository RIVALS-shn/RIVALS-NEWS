import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

def get_rivals_news():
    query = "Roblox Rivals game news"
    rss_url = f"https://google.com{query}&hl=en-US&gl=US&ceid=US:en"
    new_articles = []
    try:
        response = requests.get(rss_url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('.//item')[:3]:
                new_articles.append({
                    "title": item.find('title').text,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
    except:
        pass
    return new_articles

def update_archive():
    # Stiri de baza (se vad mereu pe site)
    static_news = [
        {"title": "🔥 NEW CODES! Use '100MVISITS' for Free Rewards! 💰", "date": "2026-04-01"},
        {"title": "🚀 CYBER UPDATE: Neon City Map is LIVE! 🏙️", "date": "2026-03-28"},
        {"title": "🏆 SEASON 5: Global Leaderboards are RESET! ✨", "date": "2026-03-25"}
    ]

    if os.path.exists('news.json'):
        try:
            with open('news.json', 'r', encoding='utf-8') as f:
                archive = json.load(f).get("articles", [])
        except:
            archive = static_news
    else:
        archive = static_news

    fresh = get_rivals_news()
    existing = {a['title'] for a in archive}
    for n in fresh:
        if n['title'] not in existing:
            archive.insert(0, n)

    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump({"last_update": datetime.now().strftime("%Y-%m-%d %H:%M"), "articles": archive[:20]}, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    update_archive()
