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
