from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('invite', views.AdminView.invite),
    path('delete', views.AdminView.delete)
]

urlpatterns = format_suffix_patterns(urlpatterns)