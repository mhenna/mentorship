from rest_framework import serializers
from rest_framework_jwt import utils

from .models import User
from answers.serializers import  AnswerSerializer
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

class UserRetrieveSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1


       