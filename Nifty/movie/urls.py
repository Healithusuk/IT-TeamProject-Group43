from django.urls import path
from .views import moviehomeView, moviedetailView, moviedetailAddFavoriteView

urlpatterns = [
    path('', moviehomeView, name = 'moviehome'),
    path('moviedetail/<int:movie_id>/', moviedetailView, name = 'moviedetail'),
    path('moviedetail/<int:movie_id>/add_to_favorite/', moviedetailAddFavoriteView, name='moviedetailaddtofavorite'),
]