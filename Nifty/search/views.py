from django.shortcuts import render
from allModels.models import Movies, Books, TvShows, Accounts

# search page function
def searchView(request):
    # Get the search query from the GET parameters; default to an empty string if not provided.
    query = request.GET.get('q', '')  
    results = []
    # If there is a search query, perform case-insensitive filtering for movies, books, and TV shows.
    if query:
        movie_results = Movies.objects.filter(movie_name__icontains=query) 
        book_results = Books.objects.filter(book_name__icontains=query) 
        tv_results = TvShows.objects.filter(tvshow_name__icontains=query)
        if query.isdigit():
            # If the query consists only of digits, assume it is an ID and search for an account with that ID.
            user_results = Accounts.objects.filter(id=query)
        else:
            # Otherwise, search for accounts where the username contains the query (case-insensitive).
            user_results = Accounts.objects.filter(username__icontains=query)
    else:
        movie_results = Movies.objects.none()
        book_results = Books.objects.none()
        tv_results = TvShows.objects.none()  
        user_results = Accounts.objects.none()
        
    context = {
        'query': query,
        'movie_results': movie_results,
        'book_results': book_results,
        'tv_results': tv_results,
        'user_results': user_results,
    }
    return render(request, 'search/search.html', context)

