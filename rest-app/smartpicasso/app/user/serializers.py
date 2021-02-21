"""
@author p.dolata
"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from smartpicasso.app.user.models import User
from smartpicasso.app.user_profile.models import UserProfile

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    """
    Class to manage serializing UserProfile
    """

    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Class to manage serializing user during registration
    """
    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            username=profile_data['username'],
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Class to manage serializing user during singing in
    """
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('An user with provided email and password is not found')
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with given email and password does not exist')

        return {'email': user.email, 'token': jwt_token}
