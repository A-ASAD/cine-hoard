from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, WatchList
from .serializers import WatchlistSerializer


class ToggleWatchlistView(APIView):
    """
    Adds or removes given movie to user's watchlist
    """

    def post(self, request, id):
        if id:
            movie = Movie.objects.filter(id=id)
            if movie.exists():
                watchlist_item = WatchList.objects.filter(
                    user=request.user,
                    movie=movie.first()
                    )
                if watchlist_item.exists():
                    watchlist_item.delete()
                    return Response({
                        'removed': f'Movie with id {id} removed from favourite'
                        })
                watchlist_item = WatchList.objects.create(
                    user=request.user,
                    movie=movie.first()
                    )
                return Response(
                    {'added': f'Movie with id {id} marked as favourite'}
                    )
            else:
                return Response({'error': 'Movie not found.'})
        return Response({'error': 'Id is invalid.'})


class GetWatchlistView(APIView):
    """
    Returns user's favourite movies
    """

    def get(self, request):
        watchlist_items = WatchList.objects.filter(user=request.user)
        if watchlist_items.exists():
            to_watch = WatchlistSerializer(
                watchlist_items.filter(is_watched=False),
                many=True
                )
            watched = WatchlistSerializer(
                watchlist_items.filter(is_watched=True),
                many=True
                )
            return Response({
                'to_watch': to_watch.data,
                'watched': watched.data
                })
        return Response({'error': 'Nothing added to watchlist yet!'})


class ToggleMarkAsWatchedView(APIView):
    """
    Toggles is_watched field on watchlist object
    """

    def post(self, request, id):
        if id:
            movie = Movie.objects.filter(id=id)
            if movie.exists():
                watchlist_item = WatchList.objects.filter(
                    user=request.user,
                    movie=movie.first()
                )
                if watchlist_item.exists():
                    watchlist_item.update(
                        is_watched=not watchlist_item.first().is_watched
                        )
                    return Response({'success': 'Watchlist updated.'})
                else:
                    return Response({'error': 'Movie not found in watchlist.'})
            else:
                return Response({'error': 'Movie not found.'})
        return Response({'error': 'Id is invalid.'})
