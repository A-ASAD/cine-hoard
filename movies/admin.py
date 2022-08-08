from django.contrib import admin

from .models import(
    Favourites,
    Genre,
    Movie,
    UserInterest,
)


admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Favourites)
admin.site.register(UserInterest)
