from django.shortcuts import render
from .models import Media, UserMedia
from .services.search import search_all
from .services.tmdb import get_popular_movies, get_popular_series, get_tmdb_genres, get_tmdb_details
from .services.books import get_popular_books, get_book_details
from .services.mal import get_popular_anime, get_mal_details
from .services.dex import get_popular_manga, get_manga_genres, get_manga_details


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

    elif category == "manga":
        genres = get_manga_genres()
        results = get_popular_manga(genre, year, page)


    elif category == "anime":
        results = get_popular_anime(genre, year, page)

    elif category == "tv":
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


def add_media(request, source, external_id):
    media = Media.objects.filter(source=source, external_id=external_id).first()

    if not media:
        data = get_tmdb_details(external_id)
        media = Media.objects.create(**data)

    UserMedia.objects.get_or_create(
        user=request.user,
        media=media
    )


def add_to_library(request, source, external_id):
    media = Media.objects.filter(source=source, external_id=external_id).first()

    if not media:
        media = fetch_and_save_from_api(source, external_id)

    UserMedia.objects.get_or_create(
        user=request.user,
        media=media
    )


def fetch_and_save_from_api(source, external_id, media_type=None):
    """
    Fetch full data from API and save to database.
    """

    # 1️⃣ Check if already exists
    media, created = Media.objects.get_or_create(
        source=source,
        external_id=external_id,
        defaults={}
    )

    if not created:
        return media

    # 2️⃣ Fetch from correct API
    if source == "tmdb":
        if not media_type:
            raise ValueError("TMDb requires media_type (movie/tv)")
        data = get_tmdb_details(external_id, media_type)

    elif source == "mal":
        data = get_mal_details(external_id)

    elif source == "books":
        data = get_book_details(external_id)

    elif source == "mangadex":
        data = get_manga_details(external_id)

    else:
        raise ValueError("Unknown source")

    # 3️⃣ Save normalized data
    media.title = data["title"]
    media.media_type = data["media_type"]
    media.release_year = data.get("release_year", "")
    media.poster = data.get("poster", "")
    media.save()

    return media

