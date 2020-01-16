from django.urls import path

from . import views

urlpatterns = [
    path('users', views.UserListCreateView.as_view()),
    path('match', views.UsersView.matchUsers),
    path('score', views.UsersView.elimination),  
    path('unmatch', views.UsersView.unMatchUsers),
    path('BUs', views.UsersView.bulk_insert_business_units),
    path('EmpLevels', views.UsersView.bulk_insert_employment_levels),
    path('getBUs', views.BusinessUnitsRetrieve.as_view()),
    path('getEmpLevels/<can_mentor>', views.EmploymentLevelsRetrieve.as_view()),
    path('business-unit-not-listed', views.EmailSendingView.business_unit_not_listed),
    path('getUserEmails', views.UsersEmailView.as_view()),      
    path('user/<email>', views.UserRetrieveView.as_view(),name='get-user'),
    # path('a', views.k.as_view()),
]