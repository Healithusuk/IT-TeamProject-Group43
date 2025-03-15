from django.shortcuts import render
from django.db.models import Q
from allModels.models import Movies, Books, TvShows, Accounts

def searchView(request):
    query = request.GET.get('q', '')  # 获取关键字，默认为空
    results = []
    if query:
        movie_results = Movies.objects.filter(movie_name__icontains=query) 
        book_results = Books.objects.filter(book_name__icontains=query) 
        tv_results = TvShows.objects.filter(tvshow_name__icontains=query)
        if query.isdigit():
            # 如果 query 仅包含数字，则认为是 id
            user_results = Accounts.objects.filter(id=query)
        else:
            # 否则认为是用户名的一部分
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

