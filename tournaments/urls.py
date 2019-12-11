from django.urls import path
from tournaments import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.tournament_list_util,name='tournament_list_util'),
    path('tournament_list/<str:message>/', views.tournament_list, name='tournament_list'),
    path('join_tournament/<int:pk>/<str:t_name>/<str:start_date>/<str:end_date>/<str:location>',
         views.join_tournament, name='join_tournament'),
    path('login/', views.login_page, name='login'),
    path('register_user/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('user_tournament/', views.user_tournament, name='user_tournament'),
    path('leave_tournament/<int:pk>', views.leave_tournament, name='leave_tournament'),
]
