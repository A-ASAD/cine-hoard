from django.db.models import Count
from django.db.models.query_utils import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Genre, Movie, Favourites
from .serializers import(
    GenresSerializer,
    MovieSerializer,
    MoviesSerializer,
)
from watchlist.models import WatchList


class GetMoviesView(APIView):
    """
    Returns specified number of movies
    """
    permission_classes = [AllowAny]

    def get(self, request, count):
        if count > 0:
            movies = MoviesSerializer(Movie.objects.all()[:count], many=True)
            return Response(movies.data)
        return Response({'error': 'Count is invalid.'})


class GetMovieDetailsView(APIView):
    """
    Returns specified movie details
    """

    def get(self, request, id):
        movie = Movie.objects.filter(id=id)
        is_favourite = False
        is_in_watchList = False
        if movie.exists():
            if Favourites.objects.filter(
                    user=request.user,
                    movies=movie.first()
                    ).exists():
                        is_favourite = True

            if WatchList.objects.filter(
                    user=request.user,
                    movie=movie.first()
                    ).exists():
                        is_in_watchList = True

            return Response({
                'data': MovieSerializer(movie, many=True).data,
                'is_favourite': is_favourite,
                'is_in_watchList': is_in_watchList,
                })
        return Response({'error': 'Movie not found.'})


class SearchMovieView(APIView):
    """
    Searches and returns movies as per search query
    """
    permission_classes = [AllowAny]

    def get(self, request, query, genre='', rating=0):
        if query:
            movies = Movie.objects.filter(title__icontains=query)
            if genre:
                movies = movies.filter(genres__name=genre)
            if rating:
                movies = movies.filter(vote_average__gte=rating)
            if movies.exists():
                movies = MoviesSerializer(movies, many=True)
                return Response(movies.data)
            else:
                return Response({'invalid_query': 'No data found.'})
        return Response({'error': 'Query is invalid.'})


class ToggleFavouriteView(APIView):
    """
    Adds or removes given movie to user's favourites
    """

    def post(self, request, id):
        if id:
            movie = Movie.objects.filter(id=id)
            if movie.exists():
                favourite = Favourites.objects.filter(
                    user=request.user,
                    movies=movie.first()
                    )
                if favourite.exists():
                    favourite.first().movies.remove(movie.first())
                    return Response({
                        'removed': f'Movie with id {id} removed from favourite'
                        })
                favourite, _ = Favourites.objects.get_or_create(
                    user=request.user
                    )
                favourite.movies.add(movie.first())
                return Response(
                    {'added': f'Movie with id {id} marked as favourite'}
                    )
            else:
                return Response({'error': 'Movie not found.'})
        return Response({'error': 'Id is invalid.'})


class GetFavouritesView(APIView):
    """
    Returns user's favourite movies
    """

    def get(self, request):
        favourites = Favourites.objects.filter(user=request.user)
        if favourites.exists():
            movies = MoviesSerializer(
                favourites.first().movies.all(),
                many=True
                )
            return Response(movies.data)
        return Response({'error': 'No favourites found'})


class GetGenresView(APIView):
    """
    Returns all the genres
    """

    def get(self, request):
        genres = GenresSerializer(Genre.objects.all(), many=True)
        return Response(genres.data)


class GetRecommendedMovies(APIView):
    """
    Returns recommended movies for user based on his
    favourite and watchlist movies (max = 20 movies)
    """

    def get(self, request):
        favourites = Favourites.objects.filter(user=request.user).first()
        watchlist = WatchList.objects.filter(user=request.user)
        genres_of_interest = set()
        if favourites.movies.exists() or watchlist:

            # get all genres from favourite movies
            if favourites:
                for movie in favourites.movies.all():
                    genres_of_interest.update(
                        [genre.id for genre in movie.genres.all()]
                        )

            # get all genres from watchlist
            if watchlist:
                for watchlist_item in watchlist:
                    watchlist_item_genres = (
                        [genre.id for genre in watchlist_item.movie.genres.all()]
                        )
                    genres_of_interest.update(watchlist_item_genres)

            # filter movies based on genres_of_interest
            movies = (
                Movie.objects.filter(vote_average__gte=7)
                .filter(genres__in=genres_of_interest)
                .annotate(movie_count=Count('id'))
                .order_by('-movie_count').distinct()
            )
            movies = MoviesSerializer(movies[:20], many=True)

            return Response(movies.data)
        return Response({'error': 'No data in favourites or watchlist yet.'})
