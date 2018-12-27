from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView
from django.http import HttpResponse
from .models import Answer
from .serializers import AnswerListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


# def index(request):
#     return HttpResponse("Hello, world. You're at the answers index.")

class AnswersListCreate(ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerListSerializer
   