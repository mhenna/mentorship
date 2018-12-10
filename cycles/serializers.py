
from rest_framework import serializers
from .models import Cycle
from users.serializers import SkillsListSerializer




class CycleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = '__all__'


class CycleSerializer(serializers.ModelSerializer):
    skills = SkillsListSerializer(many=True, read_only=True)
    class Meta:
        model = Cycle
        fields = '__all__'
        depth = 1
    