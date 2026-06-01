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
from rest_framework.views import APIView
from users.models import CustomUser

class ConfirmAPIView(APIView):

    def post(self, request):

        user_id = request.data.get('user_id')
        code = request.data.get('code')
        try: 
           confirm = ConfirmCode.objects.get(user_id=user_id)
        except  ConfirmCode.DoesNotExist:
            return Response(
                {'error': 'Confirm code not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if confirm.code == code:
            confirm.user.is_active = True
            confirm.user.save()

            confirm.is_confirmed = True
            confirm.save()
            
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    

class RegistrationAPIView(APIView):

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

        ConfirmCode.objects.create(
            user=user,
            code=code
        )
        return Response(status=status.HTTP_201_CREATED,
        data={'use_id': user.id,
            'code': code })


class AuthorizationAPIView(APIView):

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
    

