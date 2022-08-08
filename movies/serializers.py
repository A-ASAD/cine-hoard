from rest_framework import serializers

from .models import Genre, Movie


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id',
            'name',
        ]


class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'poster_path',
            'release_date',
        ]


class MovieSerializer(serializers.ModelSerializer):
    genres = GenresSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = [
            'id',
            'imdb_id',
            'title',
            'overview',
            'poster_path',
            'release_date',
            'vote_average',
            'vote_count',
            'genres'
        ]
