
from rest_framework import serializers
from .models import Cycle, Deadline, Skill, Startdate





class CycleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = '__all__'


class DeadlineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadline
        fields = '__all__'


class StartDateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startdate
        fields = '__all__'


class SkillsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class CycleSerializer(serializers.ModelSerializer):
    skills = SkillsListSerializer(many=True, read_only=True)
    class Meta:
        model = Cycle
        fields = '__all__'
        depth = 1
    

