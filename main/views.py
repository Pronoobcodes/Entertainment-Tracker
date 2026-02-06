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


def tmdb_detail_view(request, media_type, external_id):
    return detail_view(
        request,
        source="tmdb",
        external_id=external_id,
        media_type=media_type,
    )


def detail_view(request, source, external_id, media_type=None):
    if source not in ("tmdb", "mal", "mangadex"):
        return render(request, "404.html", status=404)

    item = get_details(source, external_id, media_type)

    if not item:
        return render(request, "404.html", status=404)

    # Check if item is in user's library
    in_library = False
    current_status = None

    if request.user.is_authenticated:
        media = Media.objects.filter(source=source, external_id=external_id).first()
        if media:
            user_media = UserMedia.objects.filter(user=request.user, media=media).first()
            if user_media:
                in_library = True
                current_status = user_media.status

    return render(request, "main/detail.html", {
        "item": item,
        "in_library": in_library,
        "current_status": current_status
    })


def save_media_from_api(source, external_id, media_type=None):
    # Fetch details first to ensure we have data for creation (avoids IntegrityError)
    data = get_details(source, external_id, media_type)

    if not data:
        return None

    # Use update_or_create to handle both creation and updates atomically
    media, created = Media.objects.update_or_create(
        source=source,
        external_id=external_id,
        defaults={
            "title": data.get("title"),
            "media_type": data.get("media_type", media_type),
            "release_year": data.get("release_year"),
            "poster": data.get("poster"),
        }
    )

    return media


@login_required(login_url="login")
def add_to_library(request, source=None, external_id=None, media_type=None):
    # Handle both URL parameter styles
    if source is None or external_id is None:
        return render(request, "main/404.html", status=404)
    
    media = save_media_from_api(source, external_id, media_type)

    if not media:
        return render(request, "main/404.html", status=404)

    UserMedia.objects.get_or_create(
        user=request.user,
        media=media,
        defaults={"status": "plan"}
    )

    return redirect("detail", source=source, external_id=external_id)


@login_required(login_url="login")
def tmdb_add_view(request, media_type, external_id):
    return add_to_library(
        request,
        source="tmdb",
        external_id=external_id,
        media_type=media_type,
    )


@login_required(login_url="login")
def update_status(request, media_id, status):
    user_media = get_object_or_404(
        UserMedia,
        user=request.user,
        media_id=media_id
    )
    user_media.status = status
    user_media.save()
    return redirect("profile")


@login_required(login_url="login")
def profile(request):
    user_media = UserMedia.objects.filter(user=request.user).select_related('media')
    
    watching = [m for m in user_media if m.status == 'watching']
    completed = [m for m in user_media if m.status == 'completed']
    plan = [m for m in user_media if m.status == 'plan']
    
    # Pass sections to template for cleaner rendering
    sections = [
        {"title": "Watching / Reading", "items": watching, "icon": "play-circle"},
        {"title": "Completed", "items": completed, "icon": "check-circle"},
        {"title": "Plan to Watch / Read", "items": plan, "icon": "bookmark"},
    ]
    
    return render(request, "users/profile.html", {
        "sections": sections,
        "watching": watching,
        "completed": completed,
        "plan": plan,
    })