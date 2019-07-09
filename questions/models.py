from django.db import models
import uuid
# Create your models here.
class Question(models.Model):
    
    question_text = models.CharField(max_length=300)
    is_matching = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    question_type = models.CharField(max_length=300)
    mapped = models.OneToOneField('self',default=None,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.question_text
    class Meta:
        unique_together = ('question_text', 'is_mentor')
