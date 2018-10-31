from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('questions', views.QuestionsView.creatQuestions,name='questions'),
    path('insert-questions', views.insertQuestions, name='insert-questions'),
    
]