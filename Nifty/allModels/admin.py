from django.contrib import admin
from .models import Accounts, ArtworkType, Movies, Books, TvShows, Reviews

# This page registers the backend pages of all models, 
# allowing all models to be directly manipulated by administrators on the admin page. 
# It also activates a number of features to make the default admin page work better.

class AccountsAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('id', 'username', 
                     'first_name', 
                     'last_name', 
                     'email', 
                     'is_active', 
                     'is_staff', 
                     'is_superuser', 
                     'date_joined',
                     'birthday',)
    list_editable = ('username', 
                     'first_name', 
                     'last_name', 
                     'email', 
                     'is_active', 
                     'is_staff', 
                     'is_superuser', 
                     'date_joined',
                     'birthday',)
    search_fields = ['id', 'username', 
                     'first_name', 
                     'last_name', 
                     'email', 
                     'is_active', 
                     'is_staff', 
                     'is_superuser', 
                     'date_joined',
                     'birthday',
                     ]
    list_filter = ( 'is_active', 
                    'is_staff', 
                    'is_superuser', 
                    'date_joined',
                    'birthday',)
    
    
class ReviewsAdmin(admin.ModelAdmin):
    ordering = ('review_id',)
    list_display = ( 'review_id', 
                     'user_id', 
                     'created_at', 
                     'review_content_id', 
                     'review_content_type', 
                     'rating',)
    search_fields = ['review_id', 
                     'user_id', 
                     'created_at', 
                     'review_content_id', 
                     'review_content_type', 
                     'rating',]
    list_filter = (  'created_at', 
                     'review_content_id', 
                     'review_content_type', 
                     'rating',)
class ArtworkGenreAdmin(admin.ModelAdmin):
    pass
class ArtworkTypeAdmin(admin.ModelAdmin):
    pass
class MoviesAdmin(admin.ModelAdmin):
    ordering = ('movie_id',)
    list_display = ('movie_id', 'movie_name', 
                     'movie_description', 
                     'movie_country', 
                     'movie_director', 
                     'movie_actors',
                     'movie_imdb', 
                     'movie_genre',
                     'movie_release_year')
    search_fields = ['movie_id', 'movie_name', 
                     'movie_description',  
                     'movie_country', 
                     'movie_director', 
                     'movie_actors',
                     'movie_runtime'
                     'movie_imdb', 
                     'movie_genre',
                     'movie_release_year']
    list_filter = (  'movie_country', 
                     'movie_director', 
                     'movie_actors',
                     'movie_runtime',
                     'movie_genre',
                     'movie_release_year')
class BooksAdmin(admin.ModelAdmin):
    ordering = ('book_id',)
    list_display = ('book_id', 'book_name', 
                     'book_description', 
                     'book_writer', 
                     'book_country', 
                     'book_publisher', 
                     'book_isbn', 
                     'book_rating_count', 
                     'book_average_rate',
                     'book_genre',
                     'book_release_year')
    search_fields = ['book_id', 'book_name', 
                     'book_description', 
                     'book_writer', 
                     'book_country', 
                     'book_publisher', 
                     'book_isbn', 
                     'book_rating_count', 
                     'book_average_rate',
                     'book_genre',
                     'type_id',
                     'book_release_year']
    list_filter = ( 'book_writer', 
                     'book_country', 
                     'book_publisher',  
                     'book_genre',
                     'type_id',
                     'book_release_year')
class TvShowsAdmin(admin.ModelAdmin):
    ordering = ('tvshow_id',)
    list_display = ('tvshow_id', 'tvshow_name', 
                     'tvshow_description', 
                     'tvshow_writer', 
                     'tvshow_country', 
                     'tvshow_publisher', 
                     'tvshow_imdb', 
                     'tvshow_rating_count', 
                     'tvshow_average_rate',
                     'tvshow_genre',
                     'tvshow_release_year')
    search_fields = ['tvshow_id', 'tvshow_name', 
                     'tvshow_description', 
                     'tvshow_writer', 
                     'tvshow_country', 
                     'tvshow_publisher', 
                     'tvshow_imdb', 
                     'tvshow_rating_count', 
                     'tvshow_average_rate',
                     'tvshow_genre',
                     'type_id',
                     'tvshow_release_year']
    list_filter = ( 'tvshow_writer', 
                     'tvshow_country', 
                     'tvshow_publisher',  
                     'tvshow_genre',
                     'type_id',
                     'tvshow_release_year')

admin.site.register(Accounts, AccountsAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(ArtworkType, ArtworkTypeAdmin)
admin.site.register(Movies, MoviesAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(TvShows, TvShowsAdmin)


