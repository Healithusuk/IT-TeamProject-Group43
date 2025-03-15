from django.contrib import admin
from .models import Accounts, ArtworkType, Movies, Books, TvShows, Reviews

class AccountsAdmin(admin.ModelAdmin):
    pass
class ReviewsAdmin(admin.ModelAdmin):
    pass
class ArtworkGenreAdmin(admin.ModelAdmin):
    pass
class ArtworkTypeAdmin(admin.ModelAdmin):
    pass
class MoviesAdmin(admin.ModelAdmin):
    pass
class BooksAdmin(admin.ModelAdmin):
    pass
class TvShowsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Accounts, AccountsAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(ArtworkType, ArtworkTypeAdmin)
admin.site.register(Movies, MoviesAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(TvShows, TvShowsAdmin)


