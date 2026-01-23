import requests
from django.conf import settings

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}",
}


def fetch_tmdb(endpoint, params=None):
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS,
        params=params or {},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def search_tmdb(query, page=1):
    return fetch_tmdb(
        "/search/multi",
        {
            "query": query,
            "page": page,
            "language": "en-US",
        }
    )


def normalize_tmdb(item, media_type=None):
    return {
        "source": "tmdb",
        "external_id": item["id"],
        "title": item.get("title") or item.get("name"),
        "media_type": media_type or item.get("media_type"),
        "release_year": (
            item.get("release_date")
            or item.get("first_air_date")
            or ""
        )[:4],
        "poster": (
            f"{IMAGE_BASE}{item['poster_path']}"
            if item.get("poster_path")
            else ""
        ),
    }


def get_tmdb_details(external_id, media_type):
    url = f"{BASE_URL}/{media_type}/{external_id}"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    item = response.json()

    return {
        "source": "tmdb",
        "external_id": external_id,
        "title": item.get("title") or item.get("name"),
        "media_type": media_type,
        "release_year": (item.get("release_date") or item.get("first_air_date") or "")[:4],
        "poster": f"{IMAGE_BASE}{item['poster_path']}" if item.get("poster_path") else "",
        "overview": item.get("overview"),
        "rating": item.get("vote_average"),
        "genres": [g["name"] for g in item.get("genres", [])],
        "duration": (
            item.get("runtime")
            or (item.get("episode_run_time") or [None])[0]
        ),
        "status": item.get("status", "Released"),
    }


def get_tmdb_genres(media_type):
    return fetch_tmdb(f"/genre/{media_type}/list").get("genres", [])


def get_popular_movies(genre=None, year=None, page=1):
    params = {"sort_by": "popularity.desc", "page": page}

    if genre:
        params["with_genres"] = genre
    if year:
        params["primary_release_year"] = year

    data = fetch_tmdb("/discover/movie", params)
    return [normalize_tmdb(item, "movie") for item in data.get("results", [])]


def get_popular_series(genre=None, year=None, page=1):
    params = {"sort_by": "popularity.desc", "page": page}

    if genre:
        params["with_genres"] = genre
    if year:
        params["first_air_date_year"] = year

    data = fetch_tmdb("/discover/tv", params)
    return [normalize_tmdb(item, "tv") for item in data.get("results", [])]
