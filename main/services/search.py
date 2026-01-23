from main.services.tmdb import search_tmdb
from main.services.mal import search_mal
from main.services.dex import search_dex


def search_all(query):
    results = []

    for func in (search_tmdb, search_mal, search_dex):
        try:
            results.extend(func(query))
        except Exception:
            continue

    return results