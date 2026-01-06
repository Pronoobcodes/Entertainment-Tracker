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

def get_popular_anime(genre=None, year=None):
    params = {"order_by": "popularity", "sort": "desc"}

    if genre:
        params["genres"] = genre
    if year:
        params["start_date"] = f"{year}-01-01"

    return fetch_mal("/anime", params)


def fetch_mal(endpoint, params=None):
    if params is None:
        params = {}

    headers = {
        "X-MAL-CLIENT-ID": settings.MAL_CLIENT_ID,
    }

    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    results = []

    for item in data.get("data", []):
        anime = item["node"]

        results.append({
            "source": "mal",
            "external_id": anime["id"],
            "title": anime["title"],
            "media_type": "anime",
            "release_year": (anime.get("start_date", "")[:4]),
            "poster": anime.get("main_picture", {}).get("medium", ""),
        })

    return results

