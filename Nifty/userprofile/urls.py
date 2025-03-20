from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import profileView, deleteFavorite, deleteReview, followUser, followDetail

urlpatterns = [
    path('<int:user_id>/', profileView, name = 'profile'), # profile page url
    path('<int:user_id>/delete_favorite/', deleteFavorite, name='delete_favorite'), # profile delete favorite page url
    path('<int:user_id>/delete_review/', deleteReview, name='delete_review'), # profile delete review page url
    path('<int:user_id>/follow_user/', followUser, name='follow_user'),  # profile follow user page url
    path('<int:user_id>/follow_detail/', followDetail, name='follow_detail'),  # profile follow detail page url
]