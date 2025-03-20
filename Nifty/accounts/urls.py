from django.urls import path
from .views import UserLoginView, UserRegisterView, UserLogoutView, UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # url for login page
    path('login/', UserLoginView.as_view(), name= 'login'),
    # url for register page
    path('register/', UserRegisterView.as_view(), name= 'register'),
    # url for logout page
    path('logout/', UserLogoutView.as_view(), name = 'logout'),
    # url for password_reset page
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    # url for password_reset_done page
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    # url for password_reset_email back page
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # url for password_reset_complete back page
    path('reset/done/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),  
]