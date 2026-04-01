import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def get_rivals_news():
    query = "Roblox Rivals game update news"
    rss_url = f"https://google.com{query}&hl=en-US&gl=US&ceid=US:en"
    new_articles = []
    
    try:
        response = requests.get(rss_url, timeout=10)
        root = ET.fromstring(response.content)
        for item in root.findall('.//item')[:5]:
            new_articles.append({
                "title": item.find('title').text,
                "link": item.find('link').text,
                "date": datetime.now().strftime("%Y-%m-%d") # Salvăm data salvării
            })
    except:
        pass
    return new_articles

def update_archive():
    # 1. Încercăm să citim ce avem deja salvat
    try:
        with open('news.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            archive = data.get("articles", [])
    except:
        archive = []

    # 2. Luăm știrile noi de pe net
    fresh_news = get_rivals_news()
    
    # 3. Adăugăm doar ce nu avem deja (verificăm după titlu)
    existing_titles = {art['title'] for art in archive}
    added_count = 0
    
    for news in fresh_news:
        if news['title'] not in existing_titles:
            archive.insert(0, news) # Punem știrea nouă fix la început
            added_count += 1

    # 4. Păstrăm doar ultimele 20 de știri (ca să nu devină fișierul prea mare)
    archive = archive[:20]

    # 5. Salvăm totul înapoi
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "articles": archive
    }
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"Done! Added {added_count} new items to the archive.")

if __name__ == "__main__":
    update_archive()

