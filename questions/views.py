from django.shortcuts import render
import json
from django.http import Http404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from .models import Question
from .serializers import CreateQuestionsSerializer
def index(request):
    response_data = {}
    response_data['result'] = 'error'
    response_data['message'] = 'Some error message'
    return HttpResponse(json.dumps(response_data), content_type="application/json")
class QuestionsView(APIView):

    @api_view(['POST'])
    def creatQuestions(request):
        serializer = CreateQuestionsSerializer(data=request.data['mentorQuestion'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer)
        request.data['menteeQuestion']['mapped']=serializer.data['question_id']
        menteeSerializer = CreateQuestionsSerializer(data=request.data['menteeQuestion'])
        menteeSerializer.is_valid(raise_exception=True)
        menteeSerializer.save()
        return Response(menteeSerializer.data, status=status.HTTP_200_OK)

def insertQuestions(request):
    body = request.body
    questions = json.loads(body)
    for question in questions:
        print(question['menteeQuestion']['text'])
        mentor = Question(text=question['mentorQuestion']['text'],is_matching=question['mentorQuestion']['isMatching'],question_type=question['mentorQuestion']['type'],is_mentor=True) 
        mentor.save()
        mentee = Question(text=question['menteeQuestion']['text'],is_matching=question['menteeQuestion']['isMatching'],question_type=question['menteeQuestion']['type'],is_mentor=False,mapped=mentor)     
        mentee.save()
    response_data = {}
    response_data['result'] = 'error'
    response_data['message'] ='Some error message'   
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    