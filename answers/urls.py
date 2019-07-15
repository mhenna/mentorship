from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.AnswersListCreate.as_view()),
    path('users', views.AnswersListCreateUsers.as_view()),
    path('delete', views.AnswerEditView.DeleteAnswer),
    path('edit', views.AnswerEditView.EditAnswers),
    path('getAnswers', views.AnswerListLinkUser.as_view()),
]