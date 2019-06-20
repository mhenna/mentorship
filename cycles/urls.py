from django.urls import path

from . import views

urlpatterns = [
    path('', views.CycleListCreateView.as_view()),
    path('deadline', views.AddDeadline.as_view()),
    path('edit/deadline', views.DeadlineView.Edit),
    path('edit/startdate', views.StartDateView.Edit),
    path('add/skills', views.AddSkill.as_view()),
    path('skills', views.SkillListCreateView.as_view()),
    path('delete', views.CycleEditView.DeleteCycle),
    path('edit', views.CycleEditView.EditCycle),
    path('<pk>', views.CycleRetrieveView.as_view()),

]