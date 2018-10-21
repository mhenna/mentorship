from django.test import TestCase
from .models import Question

class QuestionTestCase(TestCase):
    def setUp(self):
        Question.objects.create(text="what is your name")

    def test_create_answer(self):
        question = Question.objects.all()[0]
        self.assertEqual(question.text, "what is your name")