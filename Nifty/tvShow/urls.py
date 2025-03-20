from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import tvshowhomeView, tvshowdetailView, tvshowdetailAddFavoriteView

urlpatterns = [
    path('', tvshowhomeView, name= 'tvshowhome'), # tvshowhome page url
    path('tvshowdetail/<int:tvshow_id>/', tvshowdetailView, name = 'tvshowdetail'), # tvshowdetail page url
    path('tvshowdetail/<int:tvshow_id>/add_to_favorite/', tvshowdetailAddFavoriteView, name='tvshowdetailaddtofavorite'), # tvshowdetail add favorite page url
]