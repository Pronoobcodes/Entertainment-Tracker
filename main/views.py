from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import Media, UserMedia
from .services.search import search_all
from .services.details import get_details
from .services.tmdb import get_popular_movies, get_popular_series, get_tmdb_genres, tmdb_request
from .services.mal import get_popular_anime
from .services.dex import get_popular_manga, get_manga_genres


def home(request):
    query = request.GET.get("q")

    results = []
    if query:
        results = search_all(query)

    return render(request, "main/search.html", {
        "query": query,
        "results": results,
    })


CATEGORY_CONFIG = {
    "movies": {
        "label": "Movies",
        "fetch": get_popular_movies,
        "genres": lambda: get_tmdb_genres("movie"),
        "source": "tmdb",
        "media_type": "movie",
    },

    "series": {
        "label": "TV Series",
        "fetch": get_popular_series,
        "genres": lambda: get_tmdb_genres("tv"),
        "source": "tmdb",
        "media_type": "tv",
    },

    "anime": {
        "label": "Anime",
        "fetch": get_popular_anime,
        "genres": [],
        "source": "mal",
        "media_type": "anime",
    },

    "manga": {
        "label": "Manga",
        "fetch": get_popular_manga,
        "genres": get_manga_genres,
        "source": "mangadex",
        "media_type": "manga",
    },
}



def category_view(request, category):
    config = CATEGORY_CONFIG.get(category)

    if not config:
        return render(request, "404.html", status=404)

    genre = request.GET.get("genre")
    year = request.GET.get("year")
    page = int(request.GET.get("page", 1))

    results = config["fetch"](
        genre=genre,
        year=year,
        page=page,
    )

    current_year = datetime.now().year
    years = [str(y) for y in range(current_year, current_year - 30, -1)]
    

    genres = config["genres"]() if callable(config["genres"]) else []

    return render(request, "main/category.html", {
        "category": category,
        "label": config["label"],
        "results": results,
        "genres": genres,
        "years": years,
        "selected_genre": genre,
        "selected_year": year,
        "page": page,
    })


def detail_view(request, source, external_id, media_type=None):
    item = get_details(source, external_id, media_type)

    if not item:
        return render(request, "404.html", status=404)

    return render(request, "main/detail.html", {
        "item": item,
    })


def save_media_from_api(source, external_id, media_type=None):
    media, created = Media.objects.get_or_create(
        source=source,
        external_id=external_id,
    )

    if not created:
        return media

    data = get_details(source, external_id, media_type)

    media.title = data["title"]
    media.media_type = data["media_type"]
    media.release_year = data.get("release_year")
    media.poster = data.get("poster")
    media.save()

    return media


@login_required(login_url="login")
def add_to_library(request, source, external_id, media_type=None):
    media = save_media_from_api(source, external_id, media_type)

    UserMedia.objects.get_or_create(
        user=request.user,
        media=media,
    )

    return redirect("detail", source=source, external_id=external_id)