import re

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt import utils


class RegisterationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=15, min_length=6, required=True)
    confirm_password = serializers.CharField(max_length=15, min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def validate_username(self, value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError("Username should be unique.")
        return value

    def validate_email(self, value):
        regex = re.compile('^[a-zA-Z0-9_.+-]+@(?:(?:[a-zA-Z0-9-]+.)?[a-zA-Z]+.)?(dell|emc).com$')
        if not regex.match(value):
            raise serializers.ValidationError('Must register using a dell domain.')
        if User.objects.filter(email=value):
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_password(self, value):
        if value != self.initial_data['confirm_password']:
            raise serializers.ValidationError('Password mismatch.')
        return value

    def validate_confirm_password(self, value):
        print(self.initial_data)
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            is_superuser=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.ReadOnlyField()

    def validate_email(self, value):
        try:
             user = User.objects.get(email=value)
             self.user = user
             return value
        except User.DoesNotExist:
            raise serializers.ValidationError('Incorrect email.')

    def validate_password(self, value):
        try:
             user = User.objects.get(email=self.initial_data['email'])
             if not user.check_password(value):
                 raise serializers.ValidationError('Incorrect password')
             return value
        except User.DoesNotExist:
            return value

    def create(self, validated_data):
        payload = utils.jwt_payload_handler(self.user)
        token = utils.jwt_encode_handler(payload)
        validated_data['token'] = token
        return validated_data