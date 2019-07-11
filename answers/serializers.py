from rest_framework import serializers
from .models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ('answer_from_user',)
        depth = 1
class AnswerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class AnswerUserSerializer(serializers.ModelSerializer):
    from users.serializers import UserAnswerSerializer
    from questions.serializers import QuestionAnswerSerializer
    users = UserAnswerSerializer(source='answer_from_user')
    questions = QuestionAnswerSerializer(source='answer_to_question')
    class Meta:
        model = Answer
        fields = ('id', 'users', 'questions', 'text')