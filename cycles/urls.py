from django.urls import path

from . import views

urlpatterns = [
    path('', views.CycleListCreateView.as_view()),
    path('deadline', views.AddDeadline.as_view()),
    path('add/skills', views.AddSkill.as_view()),
    path('skills', views.CycleListView.as_view()),
    path('delete', views.CycleEditView.DeleteCycle),
    path('edit', views.CycleEditView.EditCycle),
    path('<pk>', views.CycleRetrieveView.as_view()),

]