from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser



class UserAuthenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except:
            return email
        raise ValidationError('user already exists!')