from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import bookdetailView, bookhomeView, bookdetailAddFavoriteView

urlpatterns = [
    path('', bookhomeView, name = 'bookhome'),
    path('bookdetail/<int:book_id>/', bookdetailView, name = 'bookdetail'),
    path('bookdetail/<int:book_id>/add_to_favorite/', bookdetailAddFavoriteView, name='bookdetailaddtofavorite')
]