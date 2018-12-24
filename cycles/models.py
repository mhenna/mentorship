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
    skills = models.ManyToManyField(Skill, related_name='cycles', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.name
