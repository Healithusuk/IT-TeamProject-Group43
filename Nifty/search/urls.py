from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import searchView

urlpatterns = [
    path('', searchView, name= 'search'), # seach page url
]