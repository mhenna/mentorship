from django.shortcuts import render
from rest_framework_jwt import utils

# Create your views here.
from django.shortcuts import render
from django.http import Http404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from django.http import HttpResponse
import json
from .models import User
from answers.models import Answer
from .serializers import CreateUserSerializer
from answers.serializers import AnswerListSerializer
from questions.models import Question
class UsersView(APIView):

    @api_view(['POST'])
    def createUser(request):
        userdata = {}
        for answer in request.data['answers']:
            question = Question.objects.filter(question_id=answer['questionId'])[0]
            if (not question.user_info=="None") and (not question.user_info=="")and (not question.user_info=="None"):
                for answertemp in answer['answer']:
                    request.data[question.user_info]=answertemp
        serializer = CreateUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        parsed_answers = [] 
        for question in request.data['answers']:
            for answer in question['answer']:
                if((answer['answer_id']==None) or ( answer['answer_id']=="")):
                    answer['answer_from_user']=serializer.data['user_id']
                    answer['answer_to_question'] =answer['questionId']
                    parsed_answers.append(answer)
                else :
                    tempanswer = Answer.objects.filter(answer_id=answer['answer_id'])[0]
                    tempanswer.answer_from_user.add(serializer.data['user_id'])                
                    tempanswer.save()
            answer_serializer =  AnswerListSerializer(data=parsed_answers,many=True)
            answer_serializer.is_valid(raise_exception = True)
            answer_serializer.save()
            return Response({"message":"user inserted successfully"}, status=status.HTTP_200_OK)
    @api_view(['GET'])
    def view(request,pk):
        queryset = User.objects.all()
        queryset = queryset.filter(user_id=pk)
        print(queryset)        
        serializer_class = CreateUserSerializer(queryset)
        serializer_class.is_valid()
        return Response(serializer_class.data, status=status.HTTP_200_OK)
