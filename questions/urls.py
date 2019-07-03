from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('get-questions/', views.QuestionListView.as_view(),name='get-questions'),        
    path('', views.QuestionsListCreate.as_view()),   
    path('delete', views.Edit.Delete),
    path('edit', views.Edit.EditQuestion),
    path('map', views.Edit.EditQuestionMapping), 
    path('<type>', views.QuestionsList.as_view()), 
    # path('questions', views.QuestionsView.createQuestions,name='questions'),
    # path('insert-questions', views.insertQuestions, name='insert-questions'),
 
]