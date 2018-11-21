from django.db import models

# Create your models here.
import uuid
# Create your models here.
class User(models.Model):
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
    pass
