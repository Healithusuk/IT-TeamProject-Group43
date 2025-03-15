from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import profileView, deleteFavorite, deleteReview, followUser, followDetail

urlpatterns = [
    path('<int:user_id>/', profileView, name = 'profile'),
    path('<int:user_id>/delete_favorite/', deleteFavorite, name='delete_favorite'),
    path('<int:user_id>/delete_review/', deleteReview, name='delete_review'),
    path('<int:user_id>/follow_user/', followUser, name='follow_user'),
    path('<int:user_id>/follow_detail/', followDetail, name='follow_detail'),
]