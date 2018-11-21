from rest_framework import serializers

from .models import Question
from answers.serializers import AnswerListSerializer
class CreateQuestionsSerializer(serializers.ModelSerializer):

    # certificate_name =  serializers.CharField(required=True)
    # company_id =  serializers.CharField(required=True)
    class Meta:
        model = Question
        fields = '__all__'
    def create(self, validated_data):
        return Question.objects.create(**validated_data)
    def validate_question(self, value):
        if not Question.objects.get(name=value):
            raise serializers.ValidationError('Question doesnt exist')
        return value
class QuestionListSerializer(serializers.ModelSerializer):
    answers = AnswerListSerializer(many=True, read_only=True)

    class Meta:
        model =Question
        fields = '__all__'

