import logging
import requests

from .constants import BASE_URL, LOG_FORMAT
from movies.models import Genre, Movie
from private import API_KEY


def get_raw_data(movie_id):
    """
    Fetches raw movie data from API
    """
    full_url = f'{BASE_URL}/{movie_id}?api_key={API_KEY}&language=en-US'
    return requests.get(full_url)


def add_movie(movie_data):
    """
    Creates and returns a movie
    """
    return Movie.objects.create(
        id=movie_data['id'],
        imdb_id=movie_data['imdb_id'],
        title=movie_data['original_title'],
        overview=movie_data['overview'],
        poster_path=movie_data['poster_path'],
        release_date=movie_data['release_date'],
        vote_average=movie_data['vote_average'],
        vote_count=movie_data['vote_count'],
    )


def add_genres_to_movie(movie, movie_data):
    """
    Associates genres to given movie
    """
    for genre in movie_data['genres']:
        genre_obj, _ = Genre.objects.get_or_create(
            id=genre['id'],
            name=genre['name']
        )
        movie.genres.add(genre_obj)


def get_movie_count():
    """
    Returns id of latest movie in database (movie_count)
    """
    try:
        obj = Movie.objects.latest('id')
        total_movies = obj.id + 1
    except Movie.DoesNotExist:
        total_movies = 1
    return total_movies


def get_logger(name):
    """
    Creates and return a logger with given name
    """
    logging.basicConfig(
        filename='debug.log',
        filemode='a',
        format=LOG_FORMAT,
        datefmt='%d-%b-%y %H:%M:%S',
        level=logging.INFO
    )
    logger = logging.getLogger('cinehoard')
    logger = logger.getChild(name)
    return logger
