from django.urls import path

from .views import(
    GetWatchlistView,
    ToggleMarkAsWatchedView,
    ToggleWatchlistView,
)


app_name = 'watchlist-api'

urlpatterns = [
    path('toggle-watchlist/<int:id>/', ToggleWatchlistView.as_view(), name='toggle-watchlist'),
    path('get-watchlist/', GetWatchlistView.as_view(), name='get-watchlist'),
    path('toggle-watched/<int:id>/', ToggleMarkAsWatchedView.as_view(), name='toggle-watched'),
]
