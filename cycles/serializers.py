
from rest_framework import serializers
from .models import Cycle




class CycleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = '__all__'