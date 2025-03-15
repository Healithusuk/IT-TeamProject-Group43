from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views, login
from allModels.models import Accounts

# inherits django userloginview
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'  #login html file 
    
# inherits django usercreationform
class UserRegisterView(FormView):
    template_name = 'accounts/register.html'  #register html file
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
        
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

# a view inherits logoutview in django auth
class UserLogoutView(auth_views.LogoutView):
    template_name = 'accounts/logout.html'


        
    
        
