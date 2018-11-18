from rest_framework import serializers

from .models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('answer_to_question','answer_to_user')
        depth = 1
class AnswerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'
