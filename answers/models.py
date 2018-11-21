from django.db import models

# Create your models here.
import uuid
from questions.models import Question
from users.models import User
# Create your models here.
class Answer(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=300)
    answer_to_question = models.ForeignKey(Question,related_name='answers',on_delete=models.CASCADE)
    answer_from_user = models.ManyToManyField(User, related_name='answers',default=None,null=True,blank=True)
    
    