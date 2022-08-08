from django.conf import settings
from django.db import models

from movies.models import Movie


class WatchList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user',
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='movie',
    )
    added_at = models.DateTimeField(auto_now=True)
    is_watched = models.BooleanField(default=False)
