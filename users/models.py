from django.db import models
# from dbview import DbView

# Create your models here.
import uuid
from cycles.models import Cycle, Skill
# Create your models here.


class Employee(models.Model):
    email = models.CharField(max_length=300)
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)    
    direct_manager = models.CharField(max_length=30,null=True)
    years_of_experience = models.CharField(max_length=20, null=True)
    years_within_organization = models.CharField(max_length=20, null=True)
    years_in_role = models.CharField(max_length=20, null=True)    
    study_field = models.CharField(max_length=30,null=True)
    is_mentor = models.BooleanField(default=False)
    coaching = models.BooleanField(default=False)
    work_location = models.CharField(max_length=30,null=True)
    position = models.CharField(max_length=30,null=True)
    departement = models.CharField(max_length=80,null=True)
    empLevel = models.CharField(max_length=20,null=True)
    matched = models.ManyToManyField("self",related_name='matches',blank=True)    
    skills = models.ManyToManyField(Skill, related_name='employees',blank=True)
    cycles = models.ManyToManyField(Cycle, related_name='employee',blank=True)
    capacity =  models.IntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['email'])
        ]
   
    def __str__(self):
        return self.email+" -- "+str(self.id)


class BusinessUnits(models.Model):
    business_unit = models.TextField(max_length=350)

class EmploymentLevels(models.Model):
    level = models.TextField(max_length=20)