from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField

# Create your models here.
import uuid
from questions.models import Question
from users.models import Employee
# Create your models here.
class Answer(models.Model):
    # text = HStoreField(models.CharField(max_length=100, blank=True, null = True))
    text = ArrayField(models.CharField(max_length=200), blank=True)
    answer_to_question = models.ForeignKey(Question,related_name='answers',on_delete=models.CASCADE,default=None,null=True)
    answer_from_user = models.ForeignKey(Employee, related_name='answers',default=None, null=True, on_delete=models.CASCADE)
    original =  models.BooleanField(default=False)
    
 
    def __str__(self):
        return self.text
