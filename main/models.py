from django.db import models
from django.contrib.auth import get_user_model


MEDIA_TYPE_CHOICES = [
    ("movie", "Movie"),
    ("tv", "TV Series"),
    ("anime", "Anime"),
    ("manga", "Manga"),
]

SOURCE_CHOICES = [
    ("tmdb", "TMDb"),
    ("mal", "MyAnimeList"),
    ("mangadex", "MangaDex"),
]

STATUS_CHOICES = [
    ("watching", "Watching / Reading"),
    ("completed", "Completed"),
    ("plan", "Plan to Watch / Read"),
]


class Media(models.Model):
    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)

    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    external_id = models.CharField(max_length=100)

    release_year = models.PositiveIntegerField(null=True, blank=True)
    poster = models.URLField(blank=True)
    total_episodes = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("source", "external_id")

    def __str__(self):
        return f"{self.title} ({self.media_type})"


class UserMedia(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="plan")
    progress = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "media")

    def __str__(self):
        return f"{self.user.username} → {self.media.title}"

    
