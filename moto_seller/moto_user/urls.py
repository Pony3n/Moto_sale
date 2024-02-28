from django.urls import path
from django.contrib.auth import views as auth_views

from .views import MotoRegistrationView, MotoUserProfileView

app_name = 'moto_user'

urlpatterns = [
    path('register/', MotoRegistrationView.as_view(), name='register'),
    path('profile/', MotoUserProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]