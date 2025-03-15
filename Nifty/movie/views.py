from django.shortcuts import render, get_object_or_404, redirect
from allModels.models import Movies, Reviews, ArtworkType
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def moviehomeView(request):
    query = request.GET.get('q', '')  # 获取关键字，默认为空
    if query:
        movies = Movies.objects.filter(movie_name__icontains=query) 
    else:
        movies = Movies.objects.none()
        
    context = {
        'query': query,
        'movies': movies,
    }
    return render(request, 'movie/moviehome.html', context)

def moviedetailView(request, movie_id):
    
    user = request.user
    movie = get_object_or_404(Movies, movie_id=movie_id)
    movie_ct = ArtworkType.objects.get(artwork_type="movie")
    favorited = False
    
    if request.method == "POST":
        review_text = request.POST.get('reviewText', '').strip()
        rating_value = request.POST.get('ratingwork')
        if review_text:
            review = Reviews(
                review_text=review_text,
                review_content_type=movie_ct,
                review_content_id=movie.movie_id,
                user=user,
                rating=rating_value,
            )
            review.save()
        else:
            movie.update_rating(user.pk, rating_value)
        movie.update_rating(user.pk,int(rating_value))
        
        return redirect(request.get_full_path())
    
    if user.is_authenticated:
        # favorites 存储的是字典，其中 "book" 对应一个列表
        favorites = user.favorites or {}
        movie_favorites = favorites.get("movie", [])
        favorited = any(str(fav.get('id')) == str(movie.movie_id) for fav in movie_favorites) 
      
    reviews_for_books = Reviews.objects.filter(review_content_type=movie_ct,review_content_id=movie.movie_id)        
       
    user_current_rating = movie.movie_average_rate.get(str(user.pk),0)  
    
    # 查询相同 genre 的书籍，排除当前这本书，随机取几本，比如取 5 本
    related_movies = Movies.objects.filter(movie_genre=movie.movie_genre).exclude(movie_id=movie.movie_id).order_by('?')[:10]
       
    context = {
        'movie': movie,
        'reviews_movies' : reviews_for_books,
        'user_current_rating' : user_current_rating,
        'favorited': favorited,
        'related_movies': related_movies,
    }
    return render(request, 'movie/moviedetail.html', context)

@login_required
@require_POST
def moviedetailAddFavoriteView(request, movie_id):
    # 获取 POST 数据中的类别和收藏项 ID
    category = request.POST.get('category')
    item_id = request.POST.get('item_id')
    movie = get_object_or_404(Movies, movie_id=movie_id)
    favorited = False
    # favorites 存储的是字典，其中 "book" 对应一个列表
    favorites = request.user.favorites or {}
    movie_favorites = favorites.get("movie", [])
    # 假设你存储时是以字典形式保存，并且 key 为 "id"
    # 转换为字符串，确保匹配
    favorited = any(str(fav.get('id')) == str(movie.movie_id) for fav in movie_favorites)
    
    if not category or not item_id:
        return JsonResponse({'success': False, 'message': 'Missing parameters.'})
    try:
        if(favorited):
            request.user.remove_favorite('movie', movie_id)
            action = 'removed'
        else:
            request.user.add_favorite('movie', movie_id)
            action = 'added'
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': True, 'action':action})