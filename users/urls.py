from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.UsersView.createUser, name='signup'),
    path('users', views.UserListCreateView.as_view()),
    path('user/<pk>', views.UserRetrieveView.as_view(),name='get-user')
]