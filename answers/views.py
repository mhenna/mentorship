from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView
from django.http import HttpResponse
from .models import Answer
from django.db.models import F
from django.db.models import Prefetch
from users.models import Employee
from .serializers import AnswerListSerializer, AnswerSerializer, AnswerUserSerializer, AnswerLinkUserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status


# def index(request):
#     return HttpResponse("Hello, world. You're at the answers index.")

class AnswersListCreateUsers(ListCreateAPIView):
    queryset = Answer.objects.exclude(answer_from_user__isnull=True)
    serializer_class = AnswerUserSerializer

class AnswersListCreate(ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerListSerializer 

class AnswerListLinkUser(ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerLinkUserSerializer
    

class AnswerEditView(APIView):

    @api_view(['DELETE'])
   
    def DeleteAnswer(request):
        queryset = Answer.objects.all()
        queryset = queryset.filter(id=request.data['id'])
        try:
            queryset.delete()
        except Exception as e:
            return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @api_view(['PUT'])
    def EditAnswers(request):
        query = Answer.objects.get(id=request.data['id'])
        query.text = request.data['text']        
        query.save(update_fields=['text'])
        
        serializer_class = AnswerListSerializer
        return Response(status=status.HTTP_200_OK)
