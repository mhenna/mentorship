from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-questions/', views.QuestionListView.as_view(),name='get-questions'),        
    path('get-questions/<int:mentor>', views.QuestionListCreateView.as_view(),name='get-questions'),    
    path('questions', views.QuestionsView.createQuestions,name='questions'),
    path('insert-questions', views.insertQuestions, name='insert-questions'),
 
]