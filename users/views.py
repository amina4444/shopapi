from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.serializers import (UserRegisterSerializer,UserAuthenSerializer,ConfirmationSerializer,
CustomTokenObtainPairSerializer)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import secrets
from users.models import ConfirmCode
from rest_framework.views import APIView
from users.models import CustomUser
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ConfirmAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):

        user_id = request.data.get('user_id')
        code = request.data.get('code')
        redis_code = cache.get(f"confirm code-{user_id}")

        if not redis_code:
            return Response(
                {'error': 'Confirm code not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if redis_code == code:
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            cache.delete(f"confirm code-{user_id}")
            
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            is_active=False
        )
        code = str(secrets.randbelow(1000000)).zfill(6)
        cache.set(f"confirm code-{user.id}", code,timeout=300)

        
        return Response(status=status.HTTP_201_CREATED,
        data={'use_id': user.id,
            'code': code })


class AuthorizationAPIView(CreateAPIView):
    serializer_class = UserAuthenSerializer

    def post(self, request):
        serializer = UserAuthenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email'] 
        password = serializer.validated_data['password'] 

        user = authenticate(email=email, password=password)  # user/None
        if user:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

