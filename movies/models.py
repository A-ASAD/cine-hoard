from django.conf import settings
from django.db import models


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=25, null=True)
    title = models.CharField(max_length=150)
    overview = models.TextField()
    poster_path = models.CharField(max_length=150, null=True)
    release_date = models.DateField()
    vote_average = models.DecimalField(max_digits=3, decimal_places=1)
    vote_count = models.IntegerField()
    genres = models.ManyToManyField(
        Genre,
        related_name='movie_genres'
    )


class UserInterest(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interested_user',
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='user_interest_genres'
    )


class Favourites(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_favourite',
    )
    movies = models.ManyToManyField(
        Movie,
        related_name='favourites'
    )
