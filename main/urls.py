from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("movies/", views.category_view, {"category": "movies"}, name="movies"),
    path("series/", views.category_view, {"category": "series"}, name="series"),
    path("anime/", views.category_view, {"category": "anime"}, name="anime"),
    path("mangas/", views.category_view, {"category": "manga"}, name="mangas"),
    # TMDb specific routes (must come before generic detail routes)
    path("tmdb/<str:media_type>/<str:external_id>/add/", views.tmdb_add_view, name="tmdb_add"),
    path("tmdb/<str:media_type>/<str:external_id>/", views.tmdb_detail_view, name="tmdb_detail"),
    # Update status for library items
    path("library/<int:media_id>/status/<str:status>/", views.update_status, name="update_status"),
    # Generic routes for other sources (mal, mangadex)
    path("<str:source>/<str:external_id>/add/", views.add_to_library, name="add_to_library"),
    path("<str:source>/<str:external_id>/", views.detail_view, name="detail"),
]