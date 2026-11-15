from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'learning'

urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='learning/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('science/', views.science, name='science'),
]
