from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('exam/', views.start_exam, name='exam'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.result_history, name='history'),
]