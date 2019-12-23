from rest_framework import serializers
from rest_framework_jwt import utils
from django.db.utils import IntegrityError
import re
from .models import Employee, BusinessUnits, EmploymentLevels
from answers.serializers import  AnswerSerializer

class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('email',)

class UserRetrieveSerializer(serializers.ModelSerializer):
    # answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = ('id', 'email','first_name','last_name','is_mentor', 'departement',
       'capacity','years_of_experience','years_within_organization','years_in_role',
       'matched','cycles')

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'is_mentor', 'departement', 'email', 'capacity', 'matched')

class UserListSerializer(serializers.ModelSerializer):
    def validate(self, data):
        from django.utils import timezone
        from django.db.models import Sum
        from django.utils.dateparse import parse_datetime
        from cycles.models import Deadline
        from cycles.models import Startdate
        import math
        import datetime
        import pytz
        deadline = Deadline.objects.filter(cycle=data.get('cycles')[0].id)
        start = Startdate.objects.filter(cycle=data.get('cycles')[0].id)
        
        mentee_count = Employee.objects.filter(cycles=data.get('cycles')[0].id, is_mentor=False).count()
        mentor_capacity = Employee.objects.filter(cycles=data.get('cycles')[0].id, is_mentor=True).aggregate(Sum('capacity'))
        
        if (mentor_capacity['capacity__sum'] is None):
            mentor_capacity['capacity__sum'] = 0

        if math.ceil(mentor_capacity['capacity__sum'] + (mentor_capacity['capacity__sum'] * 0.1)) <= mentee_count and mentor_capacity['capacity__sum'] != 0:
            message = 'There are too many mentees registered in this cycle. Please try next cycle.'
            raise serializers.ValidationError(message)

        now = parse_datetime(self.context['request'].data['now'])
        if data['is_mentor'] == True :
            if  (now > deadline[0].mentor_DeadlineRegistration) or (now < start[0].mentor_StartRegistration):
            #    datetime.date(datetime.today()) > form.date_deadline:
              
                message = 'You\'ve reached the deadline for the registration.'
                raise serializers.ValidationError(message)
            
        else:
            if data['is_mentor'] == False :
                if  (now > deadline[0].mentee_DeadlineRegistration) or (now < start[0].mentee_StartRegistration):
                    message = 'You\'ve reached the deadline for the registration.'
                    raise serializers.ValidationError(message)
        
        email = data.get('email')
        cycles = data.get('cycles')

        
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

class EmploymentLevelsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentLevels
        fields = '__all__'
