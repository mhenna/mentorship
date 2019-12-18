from django.db import models
import uuid


from django.utils import timezone
# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length=300,unique=True,null=True)
    type = models.CharField(max_length=30,null=True)



class Cycle(models.Model):
    name = models.CharField(max_length=30,null=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    skills = models.ManyToManyField(Skill, related_name='cycles', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

class Deadline(models.Model):
    mentor_DeadlineRegistration = models.DateTimeField(auto_now=False, auto_now_add=False)
    mentee_DeadlineRegistration = models.DateTimeField(auto_now=False, auto_now_add=False)
    cycle = models.ForeignKey(Cycle, related_name='deadline_cycle',default=None, null=True, on_delete=models.CASCADE)


class Startdate(models.Model):
    mentor_StartRegistration = models.DateTimeField(auto_now=False, auto_now_add=False)
    mentee_StartRegistration = models.DateTimeField(auto_now=False, auto_now_add=False)
    cycle = models.ForeignKey(Cycle, related_name='start_cycle',default=None, null=True, on_delete=models.CASCADE)
    
# # Create your models here.



  
