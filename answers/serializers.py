from rest_framework import serializers

from .models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('answer_id',)
        depth = 1
class AnswerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'
