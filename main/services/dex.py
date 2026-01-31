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
    res = dex_request(
        f"/manga/{external_id}",
        params={"includes[]": ["cover_art"]}
    )

    data = res.get("data")
    if not data:
        return None

    attr = data.get("attributes", {})
    title_data = attr.get("title", {})
    title = title_data.get("en") or next(iter(title_data.values()), "")

    cover = ""
    for rel in data.get("relationships", []):
        if rel["type"] == "cover_art":
            cover = f"https://uploads.mangadex.org/covers/{external_id}/{rel['attributes']['fileName']}"
            break

    genres = [
        t["attributes"]["name"]["en"]
        for t in attr.get("tags", [])
        if "en" in t["attributes"]["name"]
    ]

    return {
        "source": "mangadex",
        "external_id": external_id,
        "title": title,
        "media_type": "manga",
        "poster": cover,
        "release_year": None,
        "overview": attr.get("description", {}).get("en", ""),
        "genres": genres,
        "status": attr.get("status"),
        "rating": None,
        "duration": None,
        "episodes": None,
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