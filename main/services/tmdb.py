import requests
from django.conf import settings

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}",
}


def search_tmdb(query):
    url = f"{BASE_URL}/search/multi"
    params = {
        "query": query,
        "language": "en-US",
    }

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    results = []

    for item in data.get("results", []):
        if item.get("media_type") not in ("movie", "tv"):
            continue

        results.append({
            "source": "tmdb",
            "external_id": item["id"],
            "title": item.get("title") or item.get("name"),
            "media_type": item["media_type"],
            "release_year": (
                item.get("release_date")
                or item.get("first_air_date")
                or ""
            )[:4],
            "poster": (f"{IMAGE_BASE}{item['poster_path']}" if item.get("poster_path") else ""),
        })

    return results


def get_tmdb_details(external_id, media_type):
    url = f"{BASE_URL}/{media_type}/{external_id}"
    params = {"language": "en-US"}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    item = response.json()

    return {
        "source": "tmdb",
        "external_id": external_id,
        "title": item.get("title") or item.get("name"),
        "media_type": media_type,
        "release_year": (item.get("release_date") or item.get("first_air_date") or "")[:4],
        "poster": (f"{IMAGE_BASE}{item['poster_path']}" if item.get("poster_path") else "" ),
    }
