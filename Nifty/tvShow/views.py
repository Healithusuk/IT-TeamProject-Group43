from django.shortcuts import render, get_object_or_404, redirect
from allModels.models import TvShows, Reviews, ArtworkType
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def tvshowhomeView(request):
    # Get the search keyword from the GET parameters; default to an empty string if not provided.
    query = request.GET.get('q', '')  
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
    # Get the current logged-in user
    user = request.user
    tvshow = get_object_or_404(TvShows, tvshow_id=tvshow_id)
    tvshow_ct = ArtworkType.objects.get(artwork_type="tv")
    favorited = False
    
    # Handle POST requests, which are used for submitting a review or rating update
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
        # Retrieve the user's favorites (expected to be stored as a dictionary)
        favorites = user.favorites or {}
        tvshow_favorites = favorites.get("tv", [])
        favorited = any(str(fav.get('id')) == str(tvshow.tvshow_id) for fav in tvshow_favorites)
        
    reviews_for_tvshows = Reviews.objects.filter(review_content_type=tvshow_ct,review_content_id=tvshow.tvshow_id)        
       
    user_current_rating = tvshow.tvshow_average_rate.get(str(user.pk),0)  
    
    # Retrieve all reviews for this TV show by filtering Reviews based on its content type and ID
    related_tvshows = TvShows.objects.filter(tvshow_genre=tvshow.tvshow_genre).exclude(tvshow_id=tvshow.tvshow_id).order_by('?')[:10]
       
    context = {
        'tvshow': tvshow,
        'reviews_tvshows' : reviews_for_tvshows,
        'user_current_rating' : user_current_rating,
        'favorited': favorited,
        'related_tvshows': related_tvshows,
    }
    return render(request, 'tvShow/tvshowdetail.html', context)


@login_required  # Ensure the user is logged in before allowing access to this view.
@require_POST    # This view only accepts POST requests.
def tvshowdetailAddFavoriteView(request, tvshow_id):
    
    category = request.POST.get('category')
    item_id = request.POST.get('item_id')
    tvshow = get_object_or_404(TvShows, tvshow_id=tvshow_id)
    favorited = False
    
    favorites = request.user.favorites or {}
    tvshow_favorites = favorites.get("tv", [])
    favorited = any(str(fav.get('id')) == str(tvshow.tvshow_id) for fav in tvshow_favorites)
    
     # If either the category or item_id parameter is missing, return an error JSON response.
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
    
    # Return a JSON response indicating the operation was successful and the action taken ('added' or 'removed').
    return JsonResponse({'success': True, 'action':action})


