from django.urls import path
from .views import moviehomeView, moviedetailView, moviedetailAddFavoriteView

urlpatterns = [
    path('', moviehomeView, name = 'moviehome'), # moviehome page url
    path('moviedetail/<int:movie_id>/', moviedetailView, name = 'moviedetail'), # moviedetail page url
    path('moviedetail/<int:movie_id>/add_to_favorite/', moviedetailAddFavoriteView, name='moviedetailaddtofavorite'), # moviedetail_add_favorite page url
]