import requests
from django.conf import settings

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

HEADERS = {
    "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}",
    "accept": "application/json",
}


def tmdb_request(endpoint, params=None):
    response = requests.get(
        f"{TMDB_BASE_URL}{endpoint}",
        headers=HEADERS,
        params=params or {},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def search_tmdb(query):
    data = tmdb_request("/search/multi", {"query": query})

    results = []
    for item in data.get("results", []):
        results.append({
            "source": "tmdb",
            "external_id": item["id"],
            "title": item.get("title") or item.get("name"),
            "media_type": item.get("media_type"),
            "release_year": (item.get("release_date") or item.get("first_air_date") or "")[:4],
            "poster": TMDB_IMAGE_URL + item["poster_path"] if item.get("poster_path") else "",
        })

    return results


def get_tmdb_details(external_id, media_type):
    item = tmdb_request(f"/{media_type}/{external_id}")

    return {
        "source": "tmdb",
        "external_id": external_id,
        "title": item.get("title") or item.get("name"),
        "media_type": media_type,
        "release_year": (item.get("release_date") or item.get("first_air_date") or "")[:4],
        "poster": TMDB_IMAGE_URL + item["poster_path"] if item.get("poster_path") else "",
        "overview": item.get("overview"),
        "genres": [g["name"] for g in item.get("genres", [])],
        "rating": item.get("vote_average"),
        "duration": item.get("runtime") or (item.get("episode_run_time") or [None])[0],
        "status": item.get("status", "Released"),
    }


def get_popular_movies(genre=None, year=None, page=1):
    params = {"sort_by": "popularity.desc", "page": page}

    if genre:
        params["with_genres"] = genre
    if year:
        params["primary_release_year"] = year

    data = tmdb_request("/discover/movie", params)

    return [normalize_movie(item) for item in data["results"]]


def get_popular_series(genre=None, year=None, page=1):
    params = {"sort_by": "popularity.desc", "page": page}

    if genre:
        params["with_genres"] = genre
    if year:
        params["first_air_date_year"] = year

    data = tmdb_request("/discover/tv", params)

    return [normalize_tv(item) for item in data["results"]]


def normalize_movie(item):
    return {
        "source": "tmdb",
        "external_id": item["id"],
        "title": item["title"],
        "media_type": "movie",
        "release_year": item.get("release_date", "")[:4],
        "poster": TMDB_IMAGE_URL + item["poster_path"] if item.get("poster_path") else "",
    }


def normalize_tv(item):
    return {
        "source": "tmdb",
        "external_id": item["id"],
        "title": item["name"],
        "media_type": "tv",
        "release_year": item.get("first_air_date", "")[:4],
        "poster": TMDB_IMAGE_URL + item["poster_path"] if item.get("poster_path") else "",
    }


def get_tmdb_genres(media_type):
    data = tmdb_request(f"/genre/{media_type}/list")
    return data.get("genres", [])