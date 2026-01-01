from django.shortcuts import render
from .services.search import search_all
from .services.tmdb import get_popular_movies, get_popular_series, get_tmdb_genres
from .services.books import get_popular_books
from .services.mal import get_popular_anime
from .services.dex import get_popular_manga


def home(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = search_all(query)

    return render(request, "main/search.html", {"query": query, "results": results})



def category_view(request, category):
    genre = request.GET.get("genre")
    year = request.GET.get("year")
    page = int(request.GET.get("page", 1))

    genres = []
    results = []

    if category == "movie":
        genres = get_tmdb_genres("movie")
        results = get_popular_movies(genre, year, page)

    elif category == "book":
        
        results = get_popular_books(genre, year)

    elif category == "series":
        genres = get_tmdb_genres("series")
        results = get_popular_series(genre, year, page)

    return render(request, "main/category.html", {
        "results": results,
        "genres": genres,
        "category": category,
        "genre": genre,
        "year": year,
        "page": page,
    })

