from django.db import models

# Create your models here.
import uuid
# Create your models here.



class Skill(models.Model):
    name = models.CharField(max_length=30,unique=True,null=True)
    type = models.CharField(max_length=30,null=True)


class Employee(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=300, unique=True)
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)    
    direct_manager = models.CharField(max_length=30,null=True)
    years_of_experience = models.IntegerField(null=True)
    years_within_organization = models.IntegerField(null=True)
    years_in_role = models.IntegerField(null=True)    
    study_field = models.CharField(max_length=30,null=True)
    is_mentor = models.BooleanField(default=False)
    work_location = models.CharField(max_length=30,null=True)
    position = models.CharField(max_length=30,null=True)
    departement = models.CharField(max_length=30,null=True)
    matched = models.ManyToManyField("self",related_name='matches',default=None,blank=True)    
    skills = models.ManyToManyField(Skill, related_name='employees',default=None,blank=True)
   
    def __str__(self):
        return self.email+" -- "+str(self.user_id)


   
    # matched = models.ForeignKey('self',related_name='matches',on_delete=models.CASCADE, null=True)



    
