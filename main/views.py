from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Media, UserMedia
from .services.search import search_all
from .services.tmdb import get_popular_movies, get_popular_series, get_tmdb_genres, get_tmdb_details
from .services.mal import get_mal_details, get_popular_anime, get_mal_genres, get_mal_details
from .services.dex import get_popular_manga, get_manga_genres, get_manga_details
from .services.details import get_details
import datetime


def get_years(start=1980):
    current = datetime.datetime.now().year
    return list(range(current, start - 1, -1))


MAL_ANIME_GENRES = [
    "Action", "Adventure", "Comedy", "Drama", "Ecchi",
    "Fantasy", "Horror", "Mahou Shoujo", "Mecha",
    "Music", "Mystery", "Psychological", "Romance",
    "Sci-Fi", "Slice of Life", "Sports", "Supernatural",
    "Thriller", "Seinen", "Shoujo", "Shounen"
]

CATEGORY_MAP = {
    "movie": {
        "fetch": get_popular_movies,
        "genres": lambda: get_tmdb_genres("movie"),
        "details": get_tmdb_details,
    },
    "tv": {
        "fetch": get_popular_series,
        "genres": lambda: get_tmdb_genres("tv"),
        "details": get_tmdb_details,
    },
    "anime": {
        "fetch": get_popular_anime,
        "genres": lambda: MAL_ANIME_GENRES,
        "details": get_mal_details,
    },
    "manga": {
        "fetch": get_popular_manga,
        "genres": get_manga_genres,
        "details": get_manga_details,
    },
}


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

    config = CATEGORY_MAP.get(category)
    if not config:
        return render(request, "404.html", status=404)

    results = config["fetch"](genre=genre, year=year, page=page)

    genres = config["genres"]()

    current_year = 2026  
    years = [str(y) for y in range(current_year, current_year - 30, -1)]

    context = {
        "results": results,
        "genres": genres,
        "category": category,
        "selected_genre": genre,
        "selected_year": year,
        "page": page,
        "years": years,
    }

    return render(request, "main/category.html", context)


@login_required(login_url='login')
def detail_view(request, source, external_id, media_type=None):
    item = get_details(source, external_id, media_type)

    return render(
        request,
        "main/detail.html",
        {"item": item},
    )


@login_required(login_url='login')
def add_media(request, source, external_id):
    media = Media.objects.filter(source=source, external_id=external_id).first()

    if not media:
        data = get_tmdb_details(external_id)
        media = Media.objects.create(**data)

    UserMedia.objects.get_or_create(
        user=request.user,
        media=media
    )
    return redirect('detail', source=source, external_id=external_id)


@login_required(login_url='login')
def add_to_library(request, source, external_id):
    media = Media.objects.filter(source=source, external_id=external_id).first()

    if not media:
        media = fetch_and_save_from_api(source, external_id)

    UserMedia.objects.get_or_create(
        user=request.user,
        media=media
    )
    return redirect('detail', source=source, external_id=external_id)


def fetch_and_save_from_api(source, external_id, media_type=None):

    media, created = Media.objects.get_or_create(
        source=source,
        external_id=external_id,
        defaults={}
    )

    if not created:
        return media

    if source == "tmdb":
        if not media_type:
            raise ValueError("TMDb requires media_type (movie/tv)")
        data = get_tmdb_details(external_id, media_type)

    elif source == "mal":
        data = get_mal_details(external_id)

    elif source == "mangadex":
        data = get_manga_details(external_id)

    else:
        raise ValueError("Unknown source")

    media.title = data["title"]
    media.media_type = data["media_type"]
    media.release_year = data.get("release_year", "")
    media.poster = data.get("poster", "")
    media.save()

    return media

