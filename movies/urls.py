from django.urls import path

from .views import(
    GetFavouritesView,
    GetGenresView,
    GetMoviesView,
    GetMovieDetailsView,
    GetRecommendedMovies,
    SearchMovieView,
    ToggleFavouriteView,
)


app_name = 'movie-api'

urlpatterns = [
    path('get-movies/<int:count>/', GetMoviesView.as_view(), name='get-movies'),
    path('search/<str:query>/', SearchMovieView.as_view(), name='search-movies'),
    path('search/<int:rating>/<str:query>/', SearchMovieView.as_view(), name='search-movies'),
    path('search/<str:genre>/<str:query>/', SearchMovieView.as_view(), name='search-movies'),
    path('search/<str:genre>/<int:rating>/<str:query>/', SearchMovieView.as_view(), name='search-movies'),
    path('toggle-favourite/<int:id>/', ToggleFavouriteView.as_view(), name='toggle-favourite'),
    path('get-movie-details/<int:id>/', GetMovieDetailsView.as_view(), name='get-movie-details'),
    path('get-favourites/', GetFavouritesView.as_view(), name='get-favourites'),
    path('get-genres/', GetGenresView.as_view(), name='get-genres'),
    path('get-recommended-movies/', GetRecommendedMovies.as_view(), name='get-recommended-movies'),
]
