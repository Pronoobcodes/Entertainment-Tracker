import requests
from django.conf import settings

BASE_URL = "https://api.myanimelist.net/v2"


def fetch_mal(endpoint, params=None):
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers={"X-MAL-CLIENT-ID": settings.MAL_CLIENT_ID},
        params=params or {},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def search_mal(query, limit=10):
    data = fetch_mal(
        "/anime",
        {"q": query, "limit": limit},
    )

    return [
        {
            "source": "mal",
            "external_id": node["id"],
            "title": node["title"],
            "media_type": "anime",
            "release_year": node.get("start_date", "")[:4],
            "poster": node.get("main_picture", {}).get("medium", ""),
        }
        for item in data.get("data", [])
        for node in [item["node"]]
    ]


def normalize_mal(anime):
    return {
        "source": "mal",
        "external_id": anime["id"],
        "title": anime["title"],
        "media_type": "anime",
        "release_year": anime.get("start_date", "")[:4],
        "poster": anime.get("main_picture", {}).get("medium", ""),
    }


def get_mal_details(external_id):
    item = fetch_mal(f"/anime/{external_id}")

    return {
        "source": "mal",
        "external_id": external_id,
        "title": item["title"],
        "media_type": "anime",
        "release_year": item.get("start_date", "")[:4],
        "poster": item.get("main_picture", {}).get("large", ""),
        "overview": item.get("synopsis"),
        "rating": item.get("mean"),
        "genres": [g["name"] for g in item.get("genres", [])],
        "duration": item.get("average_episode_duration"),
        "status": item.get("status", "released").replace("_", " ").title(),
    }


def get_mal_genres():
    data = fetch_mal("/genres/anime")
    return [genre["name"] for genre in data.get("data", [])]


def get_popular_anime(genre=None, year=None, page=1, limit=20):
    offset = (page - 1) * limit

    data = fetch_mal(
        "/anime/ranking",
        {
            "ranking_type": "bypopularity",
            "limit": limit,
            "offset": offset,
        },
    )

    return [normalize_mal(item["node"]) for item in data.get("data", [])]
