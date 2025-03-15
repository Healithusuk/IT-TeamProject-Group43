from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import tvshowhomeView, tvshowdetailView, tvshowdetailAddFavoriteView

urlpatterns = [
    path('', tvshowhomeView, name= 'tvshowhome'),
    path('tvshowdetail/<int:tvshow_id>/', tvshowdetailView, name = 'tvshowdetail'),
    path('tvshowdetail/<int:tvshow_id>/add_to_favorite/', tvshowdetailAddFavoriteView, name='tvshowdetailaddtofavorite'),
]