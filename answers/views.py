from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView
from django.http import HttpResponse
from .models import Answer
from .serializers import AnswerListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status


# def index(request):
#     return HttpResponse("Hello, world. You're at the answers index.")

class AnswersListCreate(ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerListSerializer
   

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