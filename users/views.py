from django.shortcuts import render

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
from .serializers import CreateUserSerializer

class UsersView(APIView):

    @api_view(['POST'])
    def createUser(request):
        serializer = CreateUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
