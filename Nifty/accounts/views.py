from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import CustomUserCreationForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views, login
from django.http import JsonResponse
from allModels.models import Accounts
from django.contrib import messages

# inherits django userloginview
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'  #login html file 
    
    def form_invalid(self, form):
        # Loop to add an error message to the message box
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)
    
# inherits django UserRegisterView
class UserRegisterView(FormView):
    template_name = 'accounts/register.html'  # register html file
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index') # return to index
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
        
    def form_invalid(self, form):
        # Loop to add an error message to the message box
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

# a view inherits logoutview in django auth
class UserLogoutView(auth_views.LogoutView):
    template_name = 'accounts/logout.html'

# User initiates a password reset request (fill in e-mail address)
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.txt'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

# Show reminder page after reset request submission
class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

# Users enter via email link to set new passwords
class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

# Password reset completion prompt page
class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
    
        
    
        
