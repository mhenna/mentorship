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
from .serializers import UserRetrieveSerializer,UserListSerializer, BusinessUnitsListSerializer
from answers.serializers import AnswerListSerializer
from questions.models import Question
from cycles.models import Deadline
from django.utils import timezone
from cycles.models import Cycle
import string
import copy
from answers.views import AnswersListCreateUsers
from answers.serializers import AnswerUserSerializer
from django.core.mail import EmailMessage

class SendEmail(APIView):
    @api_view(['POST'])
    def send(request):
        try:
            email = EmailMessage('test', 'test', to=['nada.elsammak@emc.com', 'mostafa.henna@emc.com'])
            email.send()
        except Exception as e:
            print(e)
            return Response({'ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'EMAIL SENT'}, status=status.HTTP_200_OK)

class UserListCreateView(ListCreateAPIView):
    queryset = Employee.objects.all() # nopep8
    serializer_class = UserRetrieveSerializer

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

    def score():
        """
        Retrieve questions with 'question_type=MULTI_SELECT' and store their ids
        Loop over the ids and retrieve all answers with 'answer_to_question_id'=id
        If 'answer_from_user_id' != null and this id's 'is_mentor'=false, store 'text' and label the arrray a, b, c, 
        according to the number of options they pick
        Loop over all mentors and check the answers to the questions to calculate the score
        """

        queryset = Answer.objects.exclude(answer_from_user__isnull=True)
        serializer_class = AnswerUserSerializer

        mentor_answers, mentee_answers, mentor_answers_mcq, mentee_answers_mcq, mentee_career_mentoring, mentor_career_mentoring, mentee_career_mentoring_id, mentor_career_mentoring_id = UsersView.process_query(queryset)

        scores = {}
        max_options_size = 3
        extra_char_score = 40
        empty_slot_score = 30

        for i in mentee_answers:
            tmp_answers = []
            result = []
            tmp_answers_mentor  = []
            res_mentor = []
            actual_answer = ''
            actual_answer_mentor = ''
            this_question_id = i.answer_to_question.id
            this_mentee_id = i.answer_from_user.id
            tmp_answers = i.text

            result, actual_answer = UsersView.label_mentee_answers(tmp_answers)
            
            for j in mentor_answers:
                score = 0
                this_mentor_id = j.answer_from_user.id
                if j.answer_to_question.mapped.id == this_question_id:
                    tmp_answers_mentor = j.text
                    res_mentor = []

                    actual_answer_mentor = UsersView.label_mentor_answers(tmp_answers_mentor, tmp_answers, res_mentor, result)
            
                    score = UsersView.calculate_extra_character_or_empty_character_score(actual_answer_mentor, 
                    actual_answer, score, 
                    max_options_size,
                    empty_slot_score,
                    extra_char_score)

                    score = UsersView.calculate_mentor_answer_score(score, actual_answer_mentor, actual_answer)
                    scores = UsersView.store_mentor_score(this_mentee_id, scores, this_mentor_id, j.answer_from_user.capacity, score, j.answer_from_user.email)                
      
        return scores, mentor_answers_mcq, mentee_answers_mcq, mentee_career_mentoring_id, mentor_career_mentoring_id

    def process_query(queryset):
        mentor_answers = queryset.filter(answer_from_user__is_mentor=True, answer_to_question__question_type='MULTI_SELECT')
        mentee_answers = queryset.filter(answer_from_user__is_mentor=False, answer_to_question__question_type='MULTI_SELECT')
        mentor_answers_mcq = queryset.filter(answer_from_user__is_mentor=True, answer_to_question__question_type='MCQ')
        mentee_answers_mcq = queryset.filter(answer_from_user__is_mentor=False, answer_to_question__question_type='MCQ')
        mentee_career_mentoring =  queryset.filter(answer_from_user__is_mentor=False, text='{"Career mentoring"}')
        mentor_career_mentoring =  queryset.filter(answer_from_user__is_mentor=True, text__contains='{"Career mentoring"}')
        mentee_career_mentoring_id=[]
        mentor_career_mentoring_id=[]
        for i in mentee_career_mentoring:
            mentee_career_mentoring_id.append(i.answer_from_user.id)
        for i in mentor_career_mentoring:
            mentor_career_mentoring_id.append(i.answer_from_user.id)
        
        return mentor_answers, mentee_answers, mentor_answers_mcq, mentee_answers_mcq, mentee_career_mentoring, mentor_career_mentoring, mentee_career_mentoring_id, mentor_career_mentoring_id 

    def label_mentee_answers(tmp_answers):
        result = list(string.ascii_lowercase[0:len(tmp_answers)])
        actual_answer = ''.join(result)

        return result, actual_answer
    
    def store_mentor_score(this_mentee_id, scores, this_mentor_id, capacity, score, mentor_email):
        if this_mentee_id not in scores:
            scores[this_mentee_id] = {this_mentor_id : {'score' : score, 'capacity':capacity, 'email': mentor_email}}
        elif this_mentor_id not in scores[this_mentee_id].keys():
            scores[this_mentee_id].update({this_mentor_id : {'score': score, 'capacity':capacity, 'email': mentor_email}})
        else:
            scores[this_mentee_id][this_mentor_id]['score'] = scores[this_mentee_id][this_mentor_id]['score'] + score

        return scores

    def calculate_mentor_answer_score(score, actual_answer_mentor, actual_answer):
        ind = 0
        for p in actual_answer_mentor:
            if p is 'a' and p in actual_answer:
                score = score + (ind + 1)
            elif p is 'b' and p in actual_answer:
                score = score + (ind + 4)
            elif p is 'c' and p in actual_answer:
                score = score + (ind + 7)
            ind = ind + 1
        
        return score
    
    def calculate_extra_character_or_empty_character_score(actual_answer_mentor, actual_answer, score, max_options_size, empty_slot_score, extra_char_score):
        for q in actual_answer_mentor:
            if q not in actual_answer:
                score = score + extra_char_score
                
        if len(actual_answer_mentor) < max_options_size:
            score = score + ((max_options_size - len(actual_answer_mentor)) * empty_slot_score)
        
        return score

    def label_mentor_answers(tmp_answers_mentor, tmp_answers, res_mentor, result):
        for k in tmp_answers_mentor:
            if k in tmp_answers:
                res_mentor.append(result[tmp_answers.index(k)])
            else:
                res_mentor.append('X')

        actual_answer_mentor = ''.join(res_mentor)
        return actual_answer_mentor

    def career_mentoring_elimination(scores, mentee_career_mentoring_id, mentor_career_mentoring_id):
        refined_scores = copy.deepcopy(scores)
        for i in scores.keys():
            mentee_id = i
            if i in mentee_career_mentoring_id:
                for j in scores[i].keys():
                    if j not in mentor_career_mentoring_id:
                        del refined_scores[i][j]

        return refined_scores

    def convert_scores_to_json(sorted_scores, mentee_emails):
        returned_scores = []
        for i in sorted_scores.keys():
            mentors = []
            for j in range(len(sorted_scores[i])):
                mentors.append({'id': sorted_scores[i][j][0], 'data': sorted_scores[i][j][1]})
            
            returned_scores.append({'mentee':{'id':i, 'email': mentee_emails[i], 'mentors': mentors}})

        return returned_scores

    @api_view(['GET'])
    def elimination(request):
        scores, mentor_answers_mcq, mentee_answers_mcq, mentee_career_mentoring_id, mentor_career_mentoring_id = UsersView.score()
        sorted_scores = {}
        mentee_emails = {}
        for i in mentee_answers_mcq:
            mentee_answer = i.text
            mentee_business_unit = i.answer_from_user.departement
            question_id = i.answer_to_question.id
            mentee_emails[i.answer_from_user.id] = i.answer_from_user.email
            for j in mentor_answers_mcq:
                if question_id == 114:
                    if 'Yes' in mentee_answer:
                        if j.answer_from_user.departement == mentee_business_unit and j.answer_from_user.id in scores[i.answer_from_user.id]:
                            del scores[i.answer_from_user.id][j.answer_from_user.id]

                else:
                    if j.text != i.text and j.answer_from_user.id in scores[i.answer_from_user.id]:
                        scores[i.answer_from_user.id][j.answer_from_user.id]['score'] = scores[i.answer_from_user.id][j.answer_from_user.id]['score'] + 400

        scores = UsersView.career_mentoring_elimination(scores, mentee_career_mentoring_id, mentor_career_mentoring_id)
        
        for i in scores.keys():
            sorted_scores[i] = sorted(scores[i].items(), key = lambda x: (x[1]['score']))

        returned_scores = UsersView.convert_scores_to_json(sorted_scores, mentee_emails)
        
        return Response(returned_scores, status=status.HTTP_200_OK)

    @api_view(['POST'])    
    def matchUsers(request):
        print(request.data)
        print('mentor',request.data['menteeId'])
        print('mentor',request.data['mentorId'])
        mentor = Employee.objects.filter(id=request.data['mentorId'])[0]
        mentee = Employee.objects.filter(id=request.data['menteeId'])[0]

        if(mentor.is_mentor == mentee.is_mentor):
            return Response({'message':'You cannot match same type together'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


