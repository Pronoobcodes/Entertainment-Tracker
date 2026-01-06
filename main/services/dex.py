import requests

BASE_URL = "https://api.mangadex.org"


def search_dex(query):
    url = f"{BASE_URL}/manga"
    params = {"title": query, "limit": 10}
    data = requests.get(url, params=params).json()
    results = []

    for manga in data.get("data", []):
        attr = manga["attributes"]
        title = attr["title"].get("en") or list(attr["title"].values())[0]

        results.append({
            "source": "mangadex",
            "external_id": manga["id"],
            "title": title,
            "media_type": "manga",
            "release_year": attr.get("year"),
            "poster": "",
        })

    return results


def get_manga_details(external_id):
    url = f"{BASE_URL}/manga/{external_id}"
    manga = requests.get(url).json()["data"]
    attr = manga["attributes"]
    title = attr["title"].get("en") or list(attr["title"].values())[0]

    return {
        "source": "mangadex",
        "external_id": external_id,
        "title": title,
        "media_type": "manga",
        "release_year": attr.get("year"),
        "poster": "",
    }

def get_chapters(external_id):
    url = f"{BASE_URL}/chapter"
    params = {"manga": external_id}
    data = requests.get(url, params=params).json()
    results = []

    for chapter in data.get("data", []):
        attr = chapter["attributes"]
        results.append({
            "source": "mangadex",
            "external_id": chapter["id"],
            "title": attr.get("title"),
            "media_type": "chapter",
            "release_year": attr.get("year"),
            "poster": "",
        })

    return results

def get_chapter_details(external_id):
    url = f"{BASE_URL}/chapter/{external_id}"
    chapter = requests.get(url).json()["data"]
    attr = chapter["attributes"]

    return {
        "source": "mangadex",
        "external_id": external_id,
        "title": attr.get("title"),
        "media_type": "chapter",
        "release_year": attr.get("year"),
        "poster": "",
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

    response = requests.get(f"{BASE_URL}/manga", params=params)
    response.raise_for_status()

    return normalize_mangadex(response.json())


def normalize_mangadex(data):
    results = []

    for item in data.get("data", []):
        attrs = item["attributes"]

        title = next(iter(attrs["title"].values()), "Unknown")

        cover = ""
        for rel in item["relationships"]:
            if rel["type"] == "cover_art":
                cover = f"https://uploads.mangadex.org/covers/{item['id']}/{rel['attributes']['fileName']}"
                break

        results.append({
            "source": "mangadex",
            "external_id": item["id"],
            "title": title,
            "media_type": "manga",
            "release_year": attrs.get("year"),
            "poster": cover,
        })

    return results


def get_manga_genres():
    response = requests.get(f"{BASE_URL}/manga/tag")
    response.raise_for_status()

    return response.json().get("data", [])