from rest_framework import serializers

from .models import WatchList
from movies.serializers import(
    MovieSerializer,
)


class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    class Meta:
        model = WatchList
        fields = [
            'added_at',
            'is_watched',
            'movie',
        ]
