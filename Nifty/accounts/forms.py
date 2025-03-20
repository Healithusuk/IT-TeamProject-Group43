from django import forms
from django.contrib.auth.forms import UserCreationForm
from allModels.models import Accounts

class CustomUserCreationForm(UserCreationForm):
    class Meta:
         # set the user type to customer user type (models.Accounts)
        model = Accounts
        # set django default form fields 
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')