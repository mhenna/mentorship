from django.test import TestCase
from .models import User
from django.urls import reverse,resolve
from django.utils import timezone
import json
from faker import Factory
from faker.providers import person, python, address, profile, internet
fake = Factory.create()

class UserSingupTestCase(TestCase):
    
    def test_singup(self):
        fake.add_provider(person)
        fake.add_provider(python)
        fake.add_provider(address)
        fake.add_provider(profile)
        fake.add_provider(internet)
        user = {}
        user['first_name'] = fake.first_name()
        user['last_name'] = fake.last_name()
        user['direct_manager'] = fake.first_name()
        user['email'] = fake.safe_email()
        user['years_of_experience'] = fake.random_int(min=8, max=20)
        user['years_within_organization'] = fake.random_int(min=5, max=10)
        user['years_in_role'] = fake.random_int(min=1, max=5)
        user['is_mentor'] = fake.pybool()
        user['work_location'] = fake.city()
        user['study_field'] = fake.profile(fields='job')['job']
        user['position'] = fake.profile(fields='job')['job']
        user['departement'] = "Innovation"
        jsonObiect = json.dumps(user)
        url = reverse("signup")
        resp = self.client.post(url,jsonObiect,content_type='application/json')
        user_db = User.objects.filter(email=user['email'])[0]
        self.assertEqual(user_db.first_name,user['first_name'])
        self.assertEqual(user_db.last_name, user['last_name'])
        self.assertEqual(user_db.direct_manager, user['direct_manager'])