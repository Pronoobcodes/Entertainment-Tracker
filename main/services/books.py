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
