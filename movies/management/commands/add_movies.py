from django.core.management.base import BaseCommand
from django.db import IntegrityError

from movies.constants import MOVIES_COUNT_COMMAND
from movies.utils import(
    add_genres_to_movie,
    add_movie,
    get_logger,
    get_movie_count,
    get_raw_data,
)


# setting up logger
logger = get_logger('movies')


class Command(BaseCommand):
    help = 'Add data for first 100 movies'

    def handle(self, *args, **options):
        """
        Gets data from API and populates the database
        """

        # get latest movie id to start from
        movie_count = get_movie_count()

        # fetch and populate next configured count of movies
        for movie_id in range(movie_count, movie_count+MOVIES_COUNT_COMMAND):
            raw_movie_data = get_raw_data(movie_id)

            if raw_movie_data.status_code == 200:
                movie_data = raw_movie_data.json()
                # catch IntegrityError if movie already exists
                try:
                    movie = add_movie(movie_data)

                    # associate genres with movie
                    add_genres_to_movie(movie, movie_data)

                    logger.info(f'Movie with id {movie_id} is added!')
                except IntegrityError:
                    logger.warning(
                        f'Movie with id {movie_id} already exists!'
                        )
                except Exception as e:
                    logger.error(e)

            else:
                logger.info(
                    f'{raw_movie_data.status_code} - Movie with id {movie_id} not found!'
                    )
