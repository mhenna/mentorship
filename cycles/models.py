from django.db import models
import uuid
from users.models import Skill,Employee

# Create your models here.
class Cycle(models.Model):
    cycle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30,null=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    skills = models.ManyToManyField(Skill, related_name='cycles',default=None,blank=True)
    mentors =  models.ManyToManyField(Employee, related_name='mentors')
    mentees =  models.ManyToManyField(Employee, related_name='mentees')
    def __str__(self):
        return self.name