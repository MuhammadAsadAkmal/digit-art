from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from adminArtist.Serializers.UserSerializer import UserSerializer
from artGalleryMain.models import ArtGalleryUsers


@api_view(['POST'])
def LoginView(request):
    print(request.data)
    email = request.data.get('email')
    password = request.data.get('password')
    if email is None or password is None:
        return JsonResponse({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = ArtGalleryUsers.objects.get(email=email)
    except ArtGalleryUsers.DoesNotExist:
        return JsonResponse({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, username=user.username, password=password)
    if user is not None:
        if not user.isArtistOrAdmin():
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        # User is authenticated, return token or any other response as required
        token = Token.objects.get_or_create(user=user)
        print(token[0].key)
        return JsonResponse({
            'token': token[0].key,
            "profile": UserSerializer(user).data
        })
    else:
        # Return error message or any other response as required
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class signUp(generics.CreateAPIView):
    queryset = ArtGalleryUsers.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def signUp2(request):
    if request.method == 'POST':
        print(request.data)
