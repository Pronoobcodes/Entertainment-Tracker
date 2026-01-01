from django.urls import path
from  . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("movies/", views.category_view, {"category": "movie"}, name="movies"),
    path("series/", views.category_view, {"category": "tv"}, name="series"),
    path("anime/", views.category_view, {"category": "anime"}, name="anime"),
    path("books/", views.category_view, {"category": "book"}, name="books"),
]