from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (MotoUserRegistrationView,
                    MotoUserProfileView,
                    MotoUserLogoutView,
                    MotoUserLoginView,
                    MotoUserCreateMotorcycle,
                    MotoUserUpdateMotorcycle)

app_name = 'moto_user'

urlpatterns = [
    path('register/', MotoUserRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', MotoUserProfileView.as_view(), name='profile'),
    path('login/', MotoUserLoginView.as_view(), name='login'),
    path('logout/', MotoUserLogoutView.as_view(), name='logout'),
    path('create_motorcycle/', MotoUserCreateMotorcycle.as_view(), name='create_motorcycle'),
    path('update_motorcycle/<int:pk>', MotoUserUpdateMotorcycle.as_view(), name='update_motorcycle'),
]
