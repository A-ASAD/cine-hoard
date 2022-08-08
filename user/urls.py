from django.urls import path
from django.conf import settings
import oauth2_provider.views as oauth2_views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import(
    CustomTokenObtainPairView,
    UserCreateView,
    UserUpdateView
)


app_name = 'user-api'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register-user'),
    path('update/', UserUpdateView.as_view(), name='update-user'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.IS_AUTH_JWT:
    urlpatterns += [
        path('login/', CustomTokenObtainPairView.as_view(), name='get-token'),
    ]
else:
    urlpatterns += [
        path('login/', oauth2_views.TokenView.as_view(), name="token"),
    ]
