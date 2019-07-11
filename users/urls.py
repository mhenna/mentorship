from django.urls import path

from . import views

urlpatterns = [
    path('users', views.UserListCreateView.as_view()),
    path('match', views.UsersView.matchUsers),
    path('score', views.UsersView.elimination),  
    path('unmatch', views.UsersView.unMatchUsers),
    path('BUs', views.UsersView.bulk_insert_business_units),
    path('getBUs', views.BusinessUnitsRetrieve.as_view()),        
    path('user/<email>', views.UserRetrieveView.as_view(),name='get-user')
]