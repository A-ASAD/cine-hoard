from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from oauth2_provider.models import AccessToken
from oauth2_provider.models import RefreshToken as OAuthRefreshToken


from .serializers import(
    CustomTokenObtainPairSerializer,
    UserCreateSerializer,
    UserUpdateSerializer
)


class UserCreateView(APIView):
    """
    Creates user and returns username, email and token on success
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token = RefreshToken.for_user(
                User.objects.get(username=serializer.data['username'])
                )
            token['user'] = serializer.data['username']
            token['firstname'] = serializer.data.get('first_name', '')
            token['lastname'] = serializer.data.get('last_name', '')
            token['email'] = serializer.data['email']
            return Response({
                **serializer.data,
                'access': str(token.access_token),
                'refresh': str(token)
                })
        return Response(serializer.errors)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Returns access and refresh token on successful authentication
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserUpdateView(APIView):
    """
    Updates user details
    """

    def post(self, request):
        user = User.objects.filter(username=request.data['username'])
        if not user.exists():
            return Response({'error': 'User does not exist!'})
        serializer = UserUpdateSerializer(user.first(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            token = RefreshToken.for_user(
                User.objects.get(username=serializer.data['username'])
            )
            token['user'] = serializer.data['username']
            token['firstname'] = serializer.data['first_name']
            token['lastname'] = serializer.data['last_name']
            token['email'] = serializer.data['email']
            access_token = str(token.access_token)
            # update access token in DB if authentication is OAuth
            if not settings.IS_AUTH_JWT:
                oauth_access_token = AccessToken.objects.get(user=user.first())
                oauth_access_token.token = access_token
                oauth_access_token.save()
            return Response({
                **serializer.data,
                'access': access_token,
                'refresh': str(token)
                })
        return Response(serializer.errors)


def oauth_token_generator(request, refresh_token=False):
    """
    Token generator for OAuth
    """
    user = User.objects.get(username=request.user)
    # delete tokens from DB if already present
    oauth_access_token = AccessToken.objects.filter(user=user)
    if oauth_access_token.exists():
        oauth_access_token.delete()
    oauth_refresh_token = OAuthRefreshToken.objects.filter(user=user)
    if oauth_refresh_token.exists():
        oauth_refresh_token.delete()
    token = RefreshToken.for_user(user)
    token['user'] = user.username
    token['firstname'] = user.first_name
    token['lastname'] = user.last_name
    token['email'] = user.email
    if refresh_token:
        return str(token)
    return str(token.access_token)
