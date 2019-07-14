from rest_framework import serializers
from rest_framework_jwt import utils
from django.db.utils import IntegrityError
import re
from .models import Employee, BusinessUnits
from answers.serializers import  AnswerSerializer

class UserRetrieveSerializer(serializers.ModelSerializer):
    # answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = '__all__'

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'is_mentor', 'departement', 'email', 'capacity')

class UserListSerializer(serializers.ModelSerializer):
    def validate(self, data):
        from django.utils import timezone
        from cycles.models import Deadline
        
        deadline = Deadline.objects.first()
        now = timezone.now()
        if data['is_mentor'] == True :
            if now > deadline.mentor_DeadlineRegistration:
            #    datetime.date(datetime.today()) > form.date_deadline:
                message = 'You\'ve reached the deadline for the registration.'
                raise serializers.ValidationError(message)
        else:
            if data['is_mentor'] == False :
                if now > deadline.mentee_DeadlineRegistration:
                    message = 'You\'ve reached the deadline for the registration.'
                    raise serializers.ValidationError(message)
        
        email = data.get('email')
        cycles = data.get('cycles')
        print("***", type(cycles), " ", cycles[0].name)
        
        if Employee.objects.filter(email=email).filter(cycles=cycles[0].id):
            raise IntegrityError('Email %s already exists for cycle id %s' % (email, cycles[0].id))
        
        return data


    def validate_email(self, value):
        regex = re.compile(
            '^[a-zA-Z0-9_.+-]+@(?:(?:[a-zA-Z0-9-]+.)?[a-zA-Z]+.)?(dell|emc).com$')
        if not regex.match(value):
            raise serializers.ValidationError(
                'Must register using a dell domain.')
        # if Employee.objects.filter(email=value):
        #     raise serializers.ValidationError('Email already registered.')
        return value
    
    # def verify_uniqueness(self, data):
        
    class Meta:
        model = Employee
        fields = '__all__'

class BusinessUnitsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnits
        fields = '__all__'