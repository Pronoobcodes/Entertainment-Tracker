from django.db import models
from django.contrib.auth.models import User

MEDIA_TYPE_CHOICES = [
    ("movie", "Movie"),
    ("tv", "TV Series"),
    ("anime", "Anime"),
    ("book", "Book"),
    ("manga", "Manga"),
]

SOURCE_CHOICES = [
    ("tmdb", "TMDb"),
    ("mal", "MyAnimeList"),
    ("google_books", "Google Books"),
    ("mangadex", "MangaDex"),
]

STATUS_CHOICES = [
    ("watching", "Watching / Reading"),
    ("completed", "Completed"),
    ("on_hold", "On Hold"),
    ("dropped", "Dropped"),
    ("plan", "Plan to Watch / Read"),
]

class Media(models.Model):
    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)

    genre = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    release_year = models.PositiveIntegerField(null=True, blank=True)

    description = models.TextField(blank=True)
    cover_image = models.URLField(blank=True)

    # External API info
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    external_id = models.CharField(max_length=100)

    # Series / episodic info
    total_seasons = models.PositiveIntegerField(null=True, blank=True)
    total_episodes = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("source", "external_id")

    def __str__(self):
        return f"{self.title} ({self.media_type})"
    

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="plan")

    current_season = models.PositiveIntegerField(default=0)
    current_episode = models.PositiveIntegerField(default=0)

    rating = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "media")

    def __str__(self):
        return f"{self.user.username} - {self.media.title}"

