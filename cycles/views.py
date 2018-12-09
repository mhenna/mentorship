from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CycleListSerializer
from rest_framework.decorators import api_view
from .models import Cycle


class CycleListCreateView(ListCreateAPIView):
    queryset = Cycle.objects.all()
  
    serializer_class = CycleListSerializer


class CycleEditView(APIView):

    @api_view(['DELETE'])
    def DeleteCycle(request):
        queryset = Cycle.objects.all()
        queryset = queryset.filter(id=request.data['id'])
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['PUT'])
    def EditCycle(request):
        query = Cycle.objects.get(id=request.data['id'])
        query.start_date = request.data['start_date']
        query.end_date = request.data['end_date']
        query.deadline = request.data['deadline']
        query.name = request.data['name']
        query.save(update_fields=['start_date','end_date','deadline','name'])
        
        serializer_class = CycleListSerializer
        return Response(status=status.HTTP_200_OK)