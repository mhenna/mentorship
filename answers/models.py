from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
import uuid
from questions.models import Question
from users.models import Employee
# Create your models here.
class Answer(models.Model):
    
    text = ArrayField(models.CharField(max_length=100, blank=True))
    answer_to_question = models.ForeignKey(Question,related_name='answers',on_delete=models.CASCADE,default=None,null=True)
    answer_from_user = models.ManyToManyField(Employee, related_name='answers_from',default=None)
    
 
    def __str__(self):
        return self.text
