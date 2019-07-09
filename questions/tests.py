from django.test import TestCase
from .models import Question
from django.urls import reverse,resolve
from django.utils import timezone
import json

class QuestionTestCase(TestCase):
    # def setUp(self):
    #     # Question.objects.create(text="what is your name")

    def test_create_answer(self):
        question = {}
        question['mentorQuestion']={}
        question['mentorQuestion']['question_text']="number of expericen"
        question['mentorQuestion']['is_matching']=True
        question['mentorQuestion']['is_mentor']=True        
        question['mentorQuestion']['question_type']="MCQ"

        question['menteeQuestion']={}
        question['menteeQuestion']['question_text']="number of expericen?"
        question['menteeQuestion']['is_matching']=True
        question['menteeQuestion']['is_mentor']=False               
        question['menteeQuestion']['question_type']="MCQ"
        jsonObiect = json.dumps(question)
        url = reverse("questions")
        resp = self.client.post(url,jsonObiect,content_type='application/json')
        # print('questionsssss',Question.objects.all()[0].is_mentor,Question.objects.all()[1].is_mentor)
        mentor_question = Question.objects.filter(question_text=question['mentorQuestion']['question_text'],is_mentor=True)[0]
        mentee_question = Question.objects.filter(question_text=question['menteeQuestion']['question_text'],is_mentor=False)[0]
        self.assertEqual(mentor_question.question_text, "number of expericen")
        self.assertEqual(mentee_question.question_text, "number of expericen?")
        self.assertEqual(mentor_question.is_matching, True)
        self.assertEqual(mentee_question.is_matching, True)
        self.assertEqual(mentor_question.question_type, "MCQ")
        self.assertEqual(mentee_question.question_type, "MCQ")
        # print("mentorrrr",mentee_question.mapped)
        self.assertEqual(mentee_question.mapped, mentor_question)
        
                