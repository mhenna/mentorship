from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.UsersView.createUser, name='signup')
]