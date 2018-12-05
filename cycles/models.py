from django.db import models

from users.models import Skill
# Create your models here.
class Cycle(models.Model):
    name = models.CharField(max_length=30,null=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False)
    skills = models.ManyToManyField(Skill, related_name='cycles')