from main.services.tmdb import search_tmdb
from main.services.mal import search_mal
from main.services.books import search_books
from main.services.dex import search_dex


def search_all(query):
    results = []

    try:
        results += search_tmdb(query)
    except Exception:
        pass

    try:
        results += search_mal(query)
    except Exception:
        pass

    try:
        results += search_books(query)
    except Exception:
        pass

    try:
        results += search_dex(query)
    except Exception:
        pass

    return results
