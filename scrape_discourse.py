# scrape/scrape_discourse.py
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_URL = BASE_URL + "/c/tds-jan-2025/173.json"
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 4, 14)

def get_post_data(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    res = requests.get(url)
    return res.json()

def scrape_discourse():
    posts = []
    res = requests.get(CATEGORY_URL)
    data = res.json()

    for topic in data.get("topic_list", {}).get("topics", []):
        created_at = datetime.fromisoformat(topic["created_at"].replace("Z", ""))
        if START_DATE <= created_at <= END_DATE:
            topic_id = topic["id"]
            full_post = get_post_data(topic_id)
            for post in full_post.get("post_stream", {}).get("posts", []):
                posts.append({
                    "title": topic["title"],
                    "url": f"{BASE_URL}/t/{topic['slug']}/{topic_id}",
                    "content": post["cooked"],
                    "date": created_at.isoformat()
                })
    
    with open("app/discourse.json", "w") as f:
        json.dump(posts, f, indent=2)

if __name__ == "__main__":
    scrape_discourse()
