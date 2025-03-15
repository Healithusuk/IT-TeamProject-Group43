from django.shortcuts import render, get_object_or_404, redirect
from allModels.models import TvShows, Reviews, ArtworkType
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def tvshowhomeView(request):
    query = request.GET.get('q', '')  # 获取关键字，默认为空
    if query:
        tvshows = TvShows.objects.filter(tvshow_name__icontains=query) 
    else:
        tvshows = TvShows.objects.none()
        
    context = {
        'query': query,
        'tvshows': tvshows,
    }
    return render(request, 'tvShow/tvshowhome.html', context)

def tvshowdetailView(request, tvshow_id):
    
    user = request.user
    tvshow = get_object_or_404(TvShows, tvshow_id=tvshow_id)
    tvshow_ct = ArtworkType.objects.get(artwork_type="tv")
    favorited = False
    
    if request.method == "POST":
        review_text = request.POST.get('reviewText', '').strip()
        rating_value = request.POST.get('ratingwork')
        if review_text:
            review = Reviews(
                review_text=review_text,
                review_content_type=tvshow_ct,
                review_content_id=tvshow.tvshow_id,
                user=user,
                rating=rating_value,
            )
            review.save()
        else:
            tvshow.update_rating(user.pk, rating_value)
        tvshow.update_rating(user.pk,int(rating_value))
        
        return redirect(request.get_full_path())
    
    if user.is_authenticated:
        # favorites 存储的是字典，其中 "book" 对应一个列表
        favorites = user.favorites or {}
        tvshow_favorites = favorites.get("tv", [])
        # 假设你存储时是以字典形式保存，并且 key 为 "id"
        # 转换为字符串，确保匹配
        favorited = any(str(fav.get('id')) == str(tvshow.tvshow_id) for fav in tvshow_favorites)
        
    reviews_for_tvshows = Reviews.objects.filter(review_content_type=tvshow_ct,review_content_id=tvshow.tvshow_id)        
       
    user_current_rating = tvshow.tvshow_average_rate.get(str(user.pk),0)  
    
    # 查询相同 genre 的tvshow，排除当前这本书，随机取几本，比如取 5 本
    related_tvshows = TvShows.objects.filter(tvshow_genre=tvshow.tvshow_genre).exclude(tvshow_id=tvshow.tvshow_id).order_by('?')[:10]
       
    context = {
        'tvshow': tvshow,
        'reviews_tvshows' : reviews_for_tvshows,
        'user_current_rating' : user_current_rating,
        'favorited': favorited,
        'related_tvshows': related_tvshows,
    }
    return render(request, 'tvShow/tvshowdetail.html', context)

@login_required
@require_POST
def tvshowdetailAddFavoriteView(request, tvshow_id):
    # 获取 POST 数据中的类别和收藏项 ID
    category = request.POST.get('category')
    item_id = request.POST.get('item_id')
    tvshow = get_object_or_404(TvShows, tvshow_id=tvshow_id)
    favorited = False
    # favorites 存储的是字典，其中 "book" 对应一个列表
    favorites = request.user.favorites or {}
    tvshow_favorites = favorites.get("tv", [])
    # 假设你存储时是以字典形式保存，并且 key 为 "id"
    # 转换为字符串，确保匹配
    favorited = any(str(fav.get('id')) == str(tvshow.tvshow_id) for fav in tvshow_favorites)
    
    if not category or not item_id:
        return JsonResponse({'success': False, 'message': 'Missing parameters.'})
    try:
        if(favorited):
            request.user.remove_favorite('tv', tvshow_id)
            action = 'removed'
        else:
            request.user.add_favorite('tv', tvshow_id)
            action = 'added'
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': True, 'action':action})


