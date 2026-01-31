import requests

DEX_BASE_URL = "https://api.mangadex.org"


def dex_request(endpoint, params=None):
    response = requests.get(
        f"{DEX_BASE_URL}{endpoint}",
        params=params or {},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def format_manga(item):
    attrs = item["attributes"]
    title = next(iter(attrs["title"].values()), "Unknown")

    poster = ""
    for rel in item["relationships"]:
        if rel["type"] == "cover_art":
            poster = f"https://uploads.mangadex.org/covers/{item['id']}/{rel['attributes']['fileName']}"

    return {
        "source": "mangadex",
        "external_id": item["id"],
        "title": title,
        "media_type": "manga",
        "release_year": attrs.get("year"),
        "poster": poster,
    }


def search_manga(query):
    data = dex_request("/manga", {"title": query, "limit": 10})
    return [format_manga(item) for item in data.get("data", [])]


def get_manga_details(external_id):
    data = dex_request(f"/manga/{external_id}")
    manga = data["data"]
    attrs = manga["attributes"]

    return {
        **format_manga(manga),
        "overview": attrs.get("description", {}).get("en"),
        "genres": [
            tag["attributes"]["name"]["en"]
            for tag in attrs.get("tags", [])
            if "en" in tag["attributes"]["name"]
        ],
        "status": attrs.get("status", "released").title(),
        "duration": None,
    }


def get_popular_manga(genre=None, year=None, page=1, limit=20):
    offset = (page - 1) * limit

    params = {
        "limit": limit,
        "offset": offset,
        "order[followedCount]": "desc",
        "includes[]": ["cover_art"],
    }

    data = dex_request("/manga", params)

    return [normalize_manga(item) for item in data["data"]]


def normalize_manga(item):
    attrs = item["attributes"]
    title = next(iter(attrs["title"].values()), "Unknown")

    cover = ""
    for rel in item["relationships"]:
        if rel["type"] == "cover_art":
            cover = f"https://uploads.mangadex.org/covers/{item['id']}/{rel['attributes']['fileName']}"

    return {
        "source": "mangadex",
        "external_id": item["id"],
        "title": title,
        "media_type": "manga",
        "release_year": attrs.get("year"),
        "poster": cover,
    }


def get_manga_genres():
    data = dex_request("/manga/tag")
    return data.get("data", [])