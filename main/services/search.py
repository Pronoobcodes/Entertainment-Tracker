from .tmdb import search_tmdb
from .mal import search_anime
from .dex import search_manga

def search_all(query):
    results = []

    for search_func in (search_tmdb, search_anime, search_manga):
        try:
            results.extend(search_func(query))
        except Exception:
            continue

    return results