from django.test import TestCase
from .models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name='hossam',last_name='bahaa',direct_manager="Osama",years_of_experience=5,years_within_organization=2,years_in_role=1,study_field="cs",work_location="cairo",position="software engineer",departement="Innovation")

    def test_create_user(self):
        user = User.objects.all()[0]
        self.assertEqual(user.first_name, "hossam")