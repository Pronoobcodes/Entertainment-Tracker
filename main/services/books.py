import requests

BASE_URL = "https://www.googleapis.com/books/v1/volumes"


def search_books(query):
    params = {"q": query, "maxResults": 10}
    data = requests.get(BASE_URL, params=params).json()
    results = []

    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        results.append({
            "source": "google_books",
            "external_id": item["id"],
            "title": info.get("title", ""),
            "media_type": "book",
            "release_year": info.get("publishedDate", "")[:4],
            "poster": info.get("imageLinks", {}).get("thumbnail", ""),
        })

    return results


def get_book_details(external_id):
    url = f"{BASE_URL}/{external_id}"
    data = requests.get(url).json()
    info = data.get("volumeInfo", {})

    return {
        "source": "google_books",
        "external_id": external_id,
        "title": info.get("title", ""),
        "media_type": "book",
        "release_year": info.get("publishedDate", "")[:4],
        "poster": info.get("imageLinks", {}).get("thumbnail", ""),
    }

def get_popular_books(genre=None, year=None):
    query = "bestseller"

    if genre:
        query += f"+subject:{genre}"
    if year:
        query += f"+inpublisher:{year}"

    return fetch_books(query)


def fetch_books(query, start_index=0, max_results=20):
    params = {
        "q": query,
        "startIndex": start_index,
        "maxResults": max_results,
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    results = []

    for item in data.get("items", []):
        volume = item["volumeInfo"]

        results.append({
            "source": "books",
            "external_id": item["id"],
            "title": volume.get("title"),
            "media_type": "book",
            "release_year": (
                volume.get("publishedDate", "")[:4]
            ),
            "poster": volume.get("imageLinks", {}).get("thumbnail", ""),
        })

    return results
