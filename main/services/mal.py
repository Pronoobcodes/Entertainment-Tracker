import requests
from django.conf import settings

MAL_BASE_URL = "https://api.myanimelist.net/v2"


def mal_request(endpoint, params=None):
    response = requests.get(
        f"{MAL_BASE_URL}{endpoint}",
        headers={"X-MAL-CLIENT-ID": settings.MAL_CLIENT_ID},
        params=params or {},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def search_anime(query):
    data = mal_request("/anime", {"q": query, "limit": 10})

    results = []
    for item in data.get("data", []):
        anime = item["node"]
        results.append({
            "source": "mal",
            "external_id": anime["id"],
            "title": anime["title"],
            "media_type": "anime",
            "release_year": anime.get("start_date", "")[:4],
            "poster": anime.get("main_picture", {}).get("medium", ""),
        })

    return results


def get_mal_details(external_id):
    data = mal_request(
        f"/anime/{external_id}",
        params={
            "fields": "id,title,main_picture,synopsis,genres,mean,status,episodes"
        }
    )

    return {
        "source": "mal",
        "external_id": external_id,
        "title": data.get("title"),
        "media_type": "anime",
        "poster": data.get("main_picture", {}).get("large", ""),
        "release_year": None,
        "overview": data.get("synopsis", ""),
        "genres": [g["name"] for g in data.get("genres", [])],
        "status": data.get("status"),
        "rating": data.get("mean"),
        "episodes": data.get("episodes"),
        "duration": None,
    }


def get_popular_anime(genre=None, year=None, page=1, limit=20):
    offset = (page - 1) * limit

    data = mal_request("/anime/ranking", {
        "ranking_type": "bypopularity",
        "limit": limit,
        "offset": offset,
    })

    return [normalize_anime(item["node"]) for item in data["data"]]


def normalize_anime(item):
    return {
        "source": "mal",
        "external_id": item["id"],
        "title": item["title"],
        "media_type": "anime",
        "release_year": item.get("start_date", "")[:4],
        "poster": item.get("main_picture", {}).get("medium", ""),
    }
