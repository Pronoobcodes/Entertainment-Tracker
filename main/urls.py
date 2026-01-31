from django.urls import path
from  . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("movies/", views.category_view, {"category": "movies"}, name="movies"),
    path("series/", views.category_view, {"category": "series"}, name="series"),
    path("anime/", views.category_view, {"category": "anime"}, name="anime"),
    path("mangas/", views.category_view, {"category": "manga"}, name="mangas"),
    path('<str:source>/<str:external_id>/', views.detail_view, name='detail'),
    path('<str:source>/<str:external_id>/add/', views.add_to_library, name='add_to_library'),
]