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
from .models import Employee, Skill
from answers.models import Answer
from cycles.models import Cycle
from .serializers import CreateUserSerializer,UserRetrieveSerializer,UserListSerializer, SkillsListSerializer
from answers.serializers import AnswerListSerializer
from questions.models import Question
from cycles.models import Deadline
from django.utils import timezone
from cycles.models import Cycle

class UserListCreateView(ListCreateAPIView):
    queryset = Employee.objects.all() # nopep8
    # queryset = Company.objects.all()  # nopep8
    serializer_class = UserListSerializer
    parser_classes = (MultiPartParser,)



class SkillListCreateView(ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillsListSerializer



class AddSkill(UpdateAPIView):
    queryset= Employee.objects.all() 
    serializer_class = UserListSerializer
    def put(self, data, format=None):
        queryset = Employee.objects.get(id=self.request.data['id'])
        queryset.skills.add(self.request.data['Skill'])
        return Response(status=status.HTTP_200_OK)

def create_user(request):
        for answer in request.data['answers']:
            question = Question.objects.filter(question_id=answer['questionId'])[0]
            if (not question.user_info=="None") and (not question.user_info==""):
                for answertemp in answer['answer']:
                    request.data[question.user_info]=answertemp['text']
        serializer = CreateUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return serializer

def add_user_cycle(serializer):
        cycle = Cycle.objects.latest('creation_date')
        user = Employee.objects.get(email=serializer.data['email'])
        user.cycles.add(cycle.id)
        



def insert_answers(request,serializer):
        parsed_answers = [] 
        for question in request.data['answers']:
            for answer in question['answer']:
                if((not 'answer_id' in  answer)):       #if the answer doesn't exist in the   databse then it will create a new one using answerSerializer
                    answer_json = {}
                    answer_json['answer_from_user']=[serializer.data['id']]
                    answer_json['answer_to_question'] =question['questionId']
                    answer_json['text'] = answer['text']
                    if(not answer_json in parsed_answers):
                        parsed_answers.append(answer_json)
                else :                                                                              # else  it will just adjust the manyTomany field     
                    tempanswer = Answer.objects.filter(answer_id=answer['answer_id'])[0]
                    tempanswer.answer_from_user.add(serializer.data['id'])                
                    tempanswer.save()      
        answer_serializer =  AnswerListSerializer(data=parsed_answers,many=True)
        answer_serializer.is_valid(raise_exception = True)
        answer_serializer.save()

        
class UsersView(APIView):
    
    @api_view(['POST'])
    def signup(request):
        deadline = Deadline.objects.first()
        now = timezone.now()   
          
        
        
        if (request.data['is_mentor']==True) and (now > deadline.mentor_registration):
            return Response({"detail":"Deadline reached"}, status=status.HTTP_400_BAD_REQUEST)
        if now > deadline.mentee_registration:
            return Response({"detail":"Deadline reached"}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = create_user(request)
        user=add_user_cycle(serializer)
        insert_answers(request,user)
        return Response({"message":"user inserted successfully"}, status=status.HTTP_200_OK)


    @api_view(['POST'])    
    def matchUsers(request):
        print(request.data)
        print('mentor',request.data['menteeId'])
        print('mentor',request.data['mentorId'])
        mentor = Employee.objects.filter(id=request.data['mentorId'])[0]
        mentee = Employee.objects.filter(id=request.data['menteeId'])[0]
        mentor.matched.add(request.data['menteeId'])
        mentor.save()  
        return Response({"message":"user inserted successfully"}, status=status.HTTP_200_OK)
    
    @api_view(['POST'])    
    def unMatchUsers(request):
        print(request.data)
        print('mentor',request.data['menteeId'])
        print('mentor',request.data['mentorId'])
        mentor = Employee.objects.filter(id=request.data['mentorId'])[0]
        mentee = Employee.objects.filter(id=request.data['menteeId'])[0]
        mentor.matched.remove(request.data['menteeId'])
        mentor.save()  
        return Response({"message":"user unmatched successfully"}, status=status.HTTP_200_OK)
    
class UserRetrieveView(RetrieveAPIView):
    queryset = Employee.objects.all()     
    serializer_class = UserRetrieveSerializer
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
        # print("hereee",obj.answers.all()[0].answer_to_question.question_id)
        # answers = {}
        # for answer in obj.answers.all():
        #     answers[answer.answer_to_question.question_id] =[]
        # for answer in obj.answers.all():
        #     answers[answer.answer_to_question.question_id].append(answer)
        # print(answers,'answerssss')
        # obj.answers.set(answers)
        return obj


