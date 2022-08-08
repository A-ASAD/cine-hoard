from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
import oauth2_provider.views as oauth2_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls', namespace='user-api')),
    path('api/movies/', include('movies.urls', namespace='movie-api')),
    path('api/watchlist/', include('watchlist.urls', namespace='watchlist-api')),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    urlpatterns += [
        path("o/", include('oauth2_provider.urls', namespace='oauth2_provider')),
    ]
