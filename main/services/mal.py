import requests
from django.conf import settings

BASE_URL = "https://api.myanimelist.net/v2"


def search_mal(query):
    headers = {"X-MAL-CLIENT-ID": settings.MAL_CLIENT_ID}
    url = f"{BASE_URL}/anime"
    params = {"q": query, "limit": 10}

    data = requests.get(url, headers=headers, params=params).json()
    results = []

    for item in data.get("data", []):
        node = item["node"]
        results.append({
            "source": "mal",
            "external_id": node["id"],
            "title": node["title"],
            "media_type": "anime",
            "release_year": None,
            "poster": node.get("main_picture", {}).get("large", ""),
        })

    return results


def get_mal_details(external_id):
    headers = {"X-MAL-CLIENT-ID": settings.MAL_CLIENT_ID}
    url = f"{BASE_URL}/anime/{external_id}"

    item = requests.get(url, headers=headers).json()

    return {
        "source": "mal",
        "external_id": external_id,
        "title": item["title"],
        "media_type": "anime",
        "release_year": item.get("start_date", "")[:4],
        "poster": item.get("main_picture", {}).get("large", ""),
    }
