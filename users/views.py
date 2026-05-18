from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserRegisterSerializer,UserAuthenSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import secrets
from users.models import ConfirmCode


@api_view(['POST'])
def confirm_api_view(request):
    user_id = request.data.get('user_id')
    code = request.data.get('code')

    confirm = ConfirmCode.objects.get(user_id=user_id)

    if confirm.code == code:
        confirm.user.is_active = True
        confirm.user.save()

        confirm.is_confirmed = True
        confirm.save()
        
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )
    code = str(secrets.randbelow(1000000)).zfill(6)

    ConfirmCode.objects.create(
        user=user,
        code=code
    )
    return Response(status=status.HTTP_201_CREATED,
    data={'use_id': user.id,
          'code': code })


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username'] 
    password = serializer.validated_data['password'] 

    user = authenticate(username=username, password=password)  # user/None
    if user:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
    

