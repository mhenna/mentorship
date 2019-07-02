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
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from django.http import HttpResponse
import json
from .models import Employee, BusinessUnits
from answers.models import Answer
from cycles.models import Cycle
from .serializers import UserRetrieveSerializer,UserListSerializer, BusinessUnitsListSerializer, UserAnswerSerializer
from answers.serializers import AnswerListSerializer
from questions.models import Question
from cycles.models import Deadline
from django.utils import timezone
from cycles.models import Cycle

class UserListCreateView(ListCreateAPIView):
    queryset = Employee.objects.all() # nopep8
    serializer_class = UserAnswerSerializer

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
    def score(request):
        """
        Retrieve questions with 'question_type=MULTI_SELECT' and store their ids
        Loop over the ids and retrieve all answers with 'answer_to_question_id'=id
        If 'answer_from_user_id' != null and this id's 'is_mentor'=false, store 'text' and label the arrray a, b, c, 
        according to the number of options they pick
        Loop over all mentors and check the answers to the questions to calculate the score

        """
        query = Answer.objects.raw('SELECT answers_answer.*, users_employee.is_mentor, questions_question FROM answers_answer, questions_question, users_employee WHERE answers_answer.answer_from_user_id=users_employee.id AND questions_question.id = answers_answer.answer_to_question_id')
        mentor_answers = []

        for i in query:
            if i.answer_to_question.question_type == 'MULTI_SELECT':
                temp_obj = {'is_mentor':i.answer_from_user.is_mentor,
                'text': i.text,
                'user_id':i.answer_from_user.id,
                'answer_id':i.id}
                mentor_answers.append(temp_obj)
        
        print(mentor_answers)

        ###########################################################################################
        ###########################################################################################

        max_options_size = 3
        extra_char_score = 20
        empty_slot_score = 10
        min_score = 100000000
        mentee_answer_one = ['Finance', 'Operations', 'IT']
        labels = ['A', 'B', 'C']

        answers = dict(zip(labels, mentee_answer_one))
        actual_opttion = 'ABC'
        possible_options = ['A', 'B', 'C', 'AB', 'AC', 'BA', 'BC', 'CA', 'CB', 'ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']
        scores = {}
        for i in range(len(possible_options)):
            score = 0
            size = len(possible_options[i])
            
            for k in possible_options[i]:
                if k not in actual_opttion:
                    score = score + extra_char_score
            
            if size < max_options_size:
                score = score + ((max_options_size - size) * empty_slot_score)

            index = 0
            for j in possible_options[i]:
                if j is 'A' and j in actual_opttion:
                    score = score + (index + 1)
                elif j is 'B' and j in actual_opttion:
                    score = score + (index + 4)
                elif j is 'C' and j in actual_opttion:
                    score = score + (index + 7)

                index = index + 1
            
            if score < min_score:
                min_score = score
            scores[i]=score

        optimal_matches = []
        for key,val in scores.items():
            if val == min_score:
                optimal_matches.append(possible_options[key])
        optimal_matches.sort(key=len)
        return Response({"message":optimal_matches}, status=status.HTTP_200_OK)

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
    
    @api_view(['POST'])
    def bulk_insert_business_units(request):
        data = open('BUList.txt', 'r')
        separated_data = data.read().split('\n')
        db_entries = [
            BusinessUnits(
                business_unit=i
            )
            for i in separated_data
        ]
        BusinessUnits.objects.bulk_create(db_entries)
        return Response({"message":"hi"}, status=status.HTTP_200_OK)

class BusinessUnitsRetrieve(APIView):
    def get(self, request, format=None):
        """
        Return a list of all business units.
        """
        business_units = [bu.business_unit for bu in BusinessUnits.objects.all()]
        return Response(business_units)

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


