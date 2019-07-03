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
from .serializers import CreateQuestionsSerializer,QuestionListSerializer
# def index(request):
#     response_data = {}
#     response_data['result'] = 'error'
#     response_data['message'] = 'Some error message'
#     return HttpResponse(json.dumps(response_data), content_type="application/json")
# class QuestionsView(APIView):

#     @api_view(['POST'])
#     def createQuestions(request):
#         serializer = CreateQuestionsSerializer(data=request.data['mentorQuestion'])
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         request.data['menteeQuestion']['mapped']=serializer.data['question_id']
#         menteeSerializer = CreateQuestionsSerializer(data=request.data['menteeQuestion'])
#         menteeSerializer.is_valid(raise_exception=True)
#         menteeSerializer.save()
#         return Response(menteeSerializer.data, status=status.HTTP_200_OK)
# class QuestionListCreateView(ListCreateAPIView):
#     queryset = Question.objects.all().prefetch_related('answers') # nopep8
#     # queryset = Company.objects.all()  # nopep8
#     serializer_class = QuestionListSerializer
#     parser_classes = (MultiPartParser,)     
#     def list(self, request,mentor):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         if mentor == 0 :
#             is_mentor = True
#         else :
#             is_mentor = False 
#         queryset = Question.objects.filter(is_mentor=is_mentor).order_by('is_matching').prefetch_related('answers')
#         serializer = QuestionListSerializer(queryset, many=True)
#         return Response(serializer.data)# class QuestionRetrieveView(RetrieveAPIView):

# class QuestionListView(ListCreateAPIView):
#     queryset = Question.objects.all().prefetch_related('answers') # nopep8
#     # queryset = Company.objects.all()  # nopep8
#     serializer_class = QuestionListSerializer
#     parser_classes = (MultiPartParser,)     
#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = Question.objects.all().prefetch_related('answers') # nopep8        
#         serializer = QuestionListSerializer(queryset, many=True)
#         return Response(serializer.data)# class QuestionRetrieveView(RetrieveAPIView):

# def insertQuestions(request):
#     body = request.body
#     questions = json.loads(body)
#     for question in questions:
#         print(question['menteeQuestion']['text'])
#         mentor = Question(text=question['mentorQuestion']['text'],is_matching=question['mentorQuestion']['isMatching'],question_type=question['mentorQuestion']['type'],is_mentor=True) 
#         mentor.save()
#         mentee = Question(text=question['menteeQuestion']['text'],is_matching=question['menteeQuestion']['isMatching'],question_type=question['menteeQuestion']['type'],is_mentor=False,mapped=mentor)     
#         mentee.save()
#     response_data = {}
#     response_data['result'] = 'error'
#     response_data['message'] ='Some error message'   
#     return HttpResponse(json.dumps(response_data), content_type="application/json")

class QuestionsList(ListAPIView):
    
    serializer_class = QuestionListSerializer 
    def get_queryset(self):
        mentor = self.kwargs['type']
        queryset = Question.objects.filter(is_mentor=mentor)
        return queryset

class QuestionsListCreate(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer 

class Edit(APIView):

    @api_view(['DELETE'])
    def Delete(request):
        queryset = Question.objects.all()
        queryset = queryset.filter(id=request.data['id'])
        try:
            queryset.delete()
        except Exception as e:
            return Response({'message':'Something went wrong.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['PUT'])
    def EditQuestion(request):
        query = Question.objects.get(id=request.data['id'])
        query.is_mentor = request.data['is_mentor']
        # query.answers = request.data['answers']
        query.is_matching = request.data['is_matching']
        # query.mapped = request.data['mapped']
        query.question_text = request.data['question_text']
        query.question_type = request.data['question_type']
        
        query.save(update_fields=['question_text','question_type','is_matching', 'is_mentor', 'mapped'])
        
        serializer_class = QuestionListSerializer
        return Response(status=status.HTTP_200_OK)
    
    @api_view(['PUT'])
    def EditQuestionMapping(request):
        query = Question.objects.get(id=request.data['id'])
        tmp = Question.objects.get(id=request.data['mapped'])
        # query.is_mentor = request.data['is_mentor']
        # query.answers = request.data['answers']
        # query.is_matching = request.data['is_matching']
        # query.mapped = request.data['mapped']
        # query.question_text = request.data['question_text']
        # query.question_type = request.data['question_type']
        query.mapped = tmp
        query.save(update_fields=['mapped'])
        
        serializer_class = QuestionListSerializer
        return Response(status=status.HTTP_200_OK)