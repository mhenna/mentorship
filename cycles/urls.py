from django.urls import path

from . import views

urlpatterns = [
    path('', views.CycleListCreateView.as_view()),
    path('deadline', views.AddDeadline.as_view()),
    path('edit/deadline', views.EditDeadline.as_view()),
    path('edit/startdate', views.EditStartDate.as_view()),
    path('add/skills', views.AddSkill.as_view()),
    path('skills', views.SkillListCreateView.as_view()),
    path('delete', views.CycleEditView.DeleteCycle),
    path('edit', views.EditCycle.as_view()),
    path('<pk>', views.CycleRetrieveView.as_view()),
]