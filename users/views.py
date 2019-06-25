from django.shortcuts import render
from rest_framework_jwt import utils
from django.db.models import Count
# Create your views here.
from django.shortcuts import render
from django.http import Http404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from django.http import HttpResponse
import json
from .models import Employee
from answers.models import Answer
from cycles.models import Cycle
from .serializers import UserRetrieveSerializer,UserListSerializer
from answers.serializers import AnswerListSerializer
from questions.models import Question
from cycles.models import Deadline
from django.utils import timezone
from cycles.models import Cycle

class UserListCreateView(ListCreateAPIView):
    queryset = Employee.objects.all() # nopep8
    serializer_class = UserListSerializer

class AddSkill(APIView):
    @api_view(['PUT'])
    def create_user(request):
            queryset= Employee.objects.get(id=request.data['id'])
            print("dfvdfvsddxfvsd",queryset)
            try:
                queryset.cycles.add(request.data['cycles'])
            except Exception as e:
                print(e)
                return Response({'message':'Something went wrong.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(status=status.HTTP_200_OK)

def add_user_cycle(serializer):
        cycle = Cycle.objects.latest('creation_date')
        user = Employee.objects.get(email=serializer.data['email'])
        try:
            user.cycles.add(cycle.id)
        except Exception as e:
            print(e)
            return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
class UsersView(APIView):

    @api_view(['POST'])    
    def matchUsers(request):
        print(request.data)
        print('mentor',request.data['menteeId'])
        print('mentor',request.data['mentorId'])
        mentor = Employee.objects.filter(id=request.data['mentorId'])[0]
        mentee = Employee.objects.filter(id=request.data['menteeId'])[0]
        mentor.matched.add(request.data['menteeId'])
        try:
            mentor.save()
        except Exception as e:
            print(e)
            return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message":"user inserted successfully"}, status=status.HTTP_200_OK)
    
    @api_view(['POST'])    
    def unMatchUsers(request):
        print(request.data)
        print('mentor',request.data['menteeId'])
        print('mentor',request.data['mentorId'])
        mentor = Employee.objects.filter(id=request.data['mentorId'])[0]
        mentee = Employee.objects.filter(id=request.data['menteeId'])[0]
        mentor.matched.remove(request.data['menteeId'])
        try:
            mentor.save()
        except Exception as e:
            print(e)
            return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response({"message":"user unmatched successfully"}, status=status.HTTP_200_OK)
    
class UserRetrieveView(RetrieveAPIView):
    queryset = Employee.objects.all()     
    serializer_class = UserRetrieveSerializer
    lookup_field='email'
    def get_object(self):
        """
        Returns the object the view is displaying.
        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        queryset = queryset.filter(**filter_kwargs)
        if not queryset:
            raise Http404('Not found.')
        queryset = queryset.prefetch_related('answers')
        obj = queryset[0]
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


