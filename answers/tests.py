from django.test import TestCase

# Create your tests here.
from .models import Answer

class AnswerTestCase(TestCase):
    def setUp(self):
        Answer.objects.create(text="what is your name")

    def test_create_answer(self):
        answer = Answer.objects.all()[0]
        self.assertEqual(answer.text, "what is your name")