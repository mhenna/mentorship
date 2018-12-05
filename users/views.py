from django.shortcuts import render
from rest_framework_jwt import utils
from django.db.models import Count
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
from .models import Employee
from answers.models import Answer
from .serializers import CreateUserSerializer,UserRetrieveSerializer,UserListSerializer
from answers.serializers import AnswerListSerializer
from questions.models import Question

class UserListCreateView(ListCreateAPIView):
    queryset = Employee.objects.all() # nopep8
    # queryset = Company.objects.all()  # nopep8
    serializer_class = UserListSerializer
    parser_classes = (MultiPartParser,)

class UsersView(APIView):

    @api_view(['POST'])
    def createUser(request):
        userdata = {}
        for answer in request.data['answers']:
            question = Question.objects.filter(question_id=answer['questionId'])[0]
            if (not question.user_info=="None") and (not question.user_info=="")and (not question.user_info=="None"):
                for answertemp in answer['answer']:
                    request.data[question.user_info]=answertemp['text']
        serializer = CreateUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        parsed_answers = [] 
        print(request.data['answers'],'requestttt ')
        for question in request.data['answers']:
            for answer in question['answer']:
                if((not 'answer_id' in  answer)):
                    print('answer',answer)                
                    answer_json = {}
                    answer_json['answer_from_user']=[serializer.data['user_id']]
                    answer_json['answer_to_question'] =question['questionId']
                    answer_json['text'] = answer['text']
                    if(not answer_json in parsed_answers):
                        parsed_answers.append(answer_json)
                else :
                    tempanswer = Answer.objects.filter(answer_id=answer['answer_id'])[0]
                    tempanswer.answer_from_user.add(serializer.data['user_id'])                
                    tempanswer.save()
        print('parsedAnswers',parsed_answers)        
        answer_serializer =  AnswerListSerializer(data=parsed_answers,many=True)
        answer_serializer.is_valid(raise_exception = True)
        answer_serializer.save()
        return Response({"message":"user inserted successfully"}, status=status.HTTP_200_OK)
    @api_view(['POST'])    
    def matchUsers(request):
        print(request.data)
        print('mentor',request.data['menteeId'])
        print('mentor',request.data['mentorId'])
        mentor = Employee.objects.filter(user_id=request.data['mentorId'])[0]
        mentee = Employee.objects.filter(user_id=request.data['menteeId'])[0]
        mentor.matched.add(request.data['menteeId'])
        mentor.save()  
        return Response({"message":"user inserted successfully"}, status=status.HTTP_200_OK)
    
    @api_view(['POST'])    
    def unMatchUsers(request):
        print(request.data)
        print('mentor',request.data['menteeId'])
        print('mentor',request.data['mentorId'])
        mentor = Employee.objects.filter(user_id=request.data['mentorId'])[0]
        mentee = Employee.objects.filter(user_id=request.data['menteeId'])[0]
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


