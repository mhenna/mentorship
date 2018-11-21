from rest_framework import serializers
from rest_framework_jwt import utils

from .models import User
class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    def validate_user(self, value):
        if not User.objects.get(name=value):
            raise serializers.ValidationError('user doesnt exist ')
        return value


