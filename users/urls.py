from django.urls import path

from . import views

urlpatterns = [
    path('users', views.UserListCreateView.as_view()),
    path('match', views.UsersView.matchUsers),  
    path('unmatch', views.UsersView.unMatchUsers),        
    path('user/<email>', views.UserRetrieveView.as_view(),name='get-user')
]