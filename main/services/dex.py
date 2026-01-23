import requests
from requests.adapters import HTTPAdapter, Retry

BASE_URL = "https://api.mangadex.org"

# Create a session with retries
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))


def fetch_mangadex(endpoint, params=None):
    try:
        response = session.get(f"{BASE_URL}{endpoint}", params=params or {}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"MangaDex API request failed: {e}")
        return {"data": []}


def normalize_mangadex(data):
    results = []
    for item in data.get("data", []):
        attrs = item.get("attributes", {})
        title = next(iter(attrs.get("title", {}).values()), "Unknown")

        cover = ""
        for rel in item.get("relationships", []):
            if rel["type"] == "cover_art":
                cover = f"https://uploads.mangadex.org/covers/{item['id']}/{rel['attributes']['fileName']}"
                break

        results.append({
            "source": "mangadex",
            "external_id": item.get("id"),
            "title": title,
            "media_type": "manga",
            "release_year": attrs.get("year"),
            "poster": cover,
        })

    return results


def search_dex(query, limit=10):
    data = fetch_mangadex("/manga", {"title": query, "limit": limit})
    return normalize_mangadex(data)


def get_manga_details(external_id):
    data = fetch_mangadex(f"/manga/{external_id}")
    manga = data.get("data")
    if not manga:
        return None

    attr = manga.get("attributes", {})
    title = next(iter(attr.get("title", {}).values()), "Unknown")
    genres = [tag["attributes"]["name"]["en"] for tag in attr.get("tags", []) if "en" in tag["attributes"]["name"]]

    return {
        "source": "mangadex",
        "external_id": external_id,
        "title": title,
        "media_type": "manga",
        "release_year": attr.get("year"),
        "poster": "", 
        "overview": attr.get("description", {}).get("en"),
        "genres": genres,
        "status": attr.get("status", "released").title(),
        "duration": None,
    }


def get_popular_manga(genre=None, year=None, page=1, limit=20):
    offset = (page - 1) * limit
    params = {
        "order[followedCount]": "desc",
        "limit": limit,
        "offset": offset,
        "includes[]": ["cover_art"],
        "contentRating[]": ["safe"],
    }
    if genre:
        params["includedTags[]"] = genre
    if year:
        params["year"] = year

    data = fetch_mangadex("/manga", params)
    return normalize_mangadex(data)


def get_manga_genres():
    return fetch_mangadex("/manga/tag").get("data", [])
