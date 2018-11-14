from django.db import models

# Create your models here.
import uuid
# Create your models here.
class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=300, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)    
    direct_manager = models.CharField(max_length=30)
    years_of_experience = models.IntegerField()
    years_within_organization = models.IntegerField()
    years_in_role = models.IntegerField()    
    study_field = models.CharField(max_length=30)
    is_mentor = models.BooleanField(default=False)
    work_location = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    departement = models.CharField(max_length=30)
