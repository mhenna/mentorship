from rest_framework import serializers
from rest_framework_jwt import utils
import re
from .models import Employee
from answers.serializers import  AnswerSerializer
class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'
    def create(self, validated_data):
        return Employee.objects.create(**validated_data)
    def validate_user(self, value):
        if not Employee.objects.get(name=value):
            raise serializers.ValidationError('user doesnt exist ')
        return value

class UserRetrieveSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = '__all__'

class UserListSerializer(serializers.ModelSerializer):
    def validate(self, data):
        from django.utils import timezone
        from cycles.models import Deadline
        
        deadline = Deadline.objects.first()
        now = timezone.now()
        if data['is_mentor'] == True :
            if now > deadline.mentor_registration:
            #    datetime.date(datetime.today()) > form.date_deadline:
                message = 'You\'ve reached the deadline for the registration.'
                raise serializers.ValidationError(message)
        else:
            if data['is_mentor'] == False :
                if now > deadline.mentee_registration:
                    message = 'You\'ve reached the deadline for the registration.'
                    raise serializers.ValidationError(message)

        return data


    def validate_email(self, value):
        regex = re.compile(
            '^[a-zA-Z0-9_.+-]+@(?:(?:[a-zA-Z0-9-]+.)?[a-zA-Z]+.)?(dell|emc).com$')
        if not regex.match(value):
            raise serializers.ValidationError(
                'Must register using a dell domain.')
        if Employee.objects.filter(email=value):
            raise serializers.ValidationError('Email already registered.')
        return value
    class Meta:
        model = Employee
        fields = '__all__'
        


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
