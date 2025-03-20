from django.shortcuts import render, get_object_or_404, redirect
from allModels.models import Movies, Reviews, ArtworkType
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# moviehome page function
def moviehomeView(request):
    # Retrieve the search keyword from the GET parameter 'q', defaulting to an empty string if not provided.
    query = request.GET.get('q', '')  
    if query:
        movies = Movies.objects.filter(movie_name__icontains=query) 
    else:
        movies = Movies.objects.none()
        
    context = {
        'query': query,
        'movies': movies,
    }
    return render(request, 'movie/moviehome.html', context)

# moviedetail page function
def moviedetailView(request, movie_id):
    # Get the current logged-in user
    user = request.user
    movie = get_object_or_404(Movies, movie_id=movie_id)
    movie_ct = ArtworkType.objects.get(artwork_type="movie")
    favorited = False
    
    # Handle POST requests (when submitting a review or rating)
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
    
    # If the user is authenticated, check if the book is already in their favorites
    if user.is_authenticated:
        favorites = user.favorites or {}
        movie_favorites = favorites.get("movie", [])
        favorited = any(str(fav.get('id')) == str(movie.movie_id) for fav in movie_favorites) 
      
    reviews_for_books = Reviews.objects.filter(review_content_type=movie_ct,review_content_id=movie.movie_id)        
    user_current_rating = movie.movie_average_rate.get(str(user.pk),0)  
    
    # Query for related books with the same genre, excluding the current book,
    # and randomly order them; select up to 10 related books.
    related_movies = Movies.objects.filter(movie_genre=movie.movie_genre).exclude(movie_id=movie.movie_id).order_by('?')[:10]
       
    context = {
        'movie': movie,
        'reviews_movies' : reviews_for_books,
        'user_current_rating' : user_current_rating,
        'favorited': favorited,
        'related_movies': related_movies,
    }
    return render(request, 'movie/moviedetail.html', context)

@login_required  # Ensure the user is logged in before accessing this view.
@require_POST    # Only allow POST requests for this view.
def moviedetailAddFavoriteView(request, movie_id):
    
    # Retrieve the 'category' and 'item_id' parameters from the POST data.
    category = request.POST.get('category')
    item_id = request.POST.get('item_id')
    movie = get_object_or_404(Movies, movie_id=movie_id)
    favorited = False

    favorites = request.user.favorites or {}
    movie_favorites = favorites.get("movie", [])
  
    favorited = any(str(fav.get('id')) == str(movie.movie_id) for fav in movie_favorites)
    
    # If either the category or item_id is missing, return a JSON error response.
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
    
    # Return a JSON response indicating the success of the operation and the action taken.
    return JsonResponse({'success': True, 'action':action})