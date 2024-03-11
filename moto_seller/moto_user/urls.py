from django.urls import path
from django.contrib.auth import views as auth_views

from .views import MotoRegistrationView, MotoUserProfileView, MotoUserLogoutView, MotoUserLoginView

app_name = 'moto_user'

urlpatterns = [
    path('register/', MotoRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', MotoUserProfileView.as_view(), name='profile'),
    path('login/', MotoUserLoginView.as_view(), name='login'),
    path('logout/', MotoUserLogoutView.as_view(), name='logout'),
]
