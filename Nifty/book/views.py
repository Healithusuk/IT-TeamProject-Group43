from django.shortcuts import render, get_object_or_404, redirect
from allModels.models import Books, Reviews, ArtworkType
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# bookhome page function
def bookhomeView(request):
    # Retrieve the search keyword from the GET parameter 'q', defaulting to an empty string if not provided.
    query = request.GET.get('q', '')  
    if query:
        books = Books.objects.filter(book_name__icontains=query) 
    else:
        books = Books.objects.none()
        
    context = {
        'query': query,
        'books': books,
    }
    return render(request, 'book/bookhome.html', context)

# bookdetail page function
def bookdetailView(request, book_id):
    # Get the current logged-in user
    user = request.user
    book = get_object_or_404(Books, book_id=book_id)
    book_ct = ArtworkType.objects.get(artwork_type="book")
    favorited = False
    
    # Handle POST requests (when submitting a review or rating)
    if request.method == "POST":
        review_text = request.POST.get('reviewText', '').strip()
        rating_value = request.POST.get('ratingwork')
        if review_text:
            review = Reviews(
                review_text=review_text,
                review_content_type=book_ct,
                review_content_id=book.book_id,
                user=user,
                rating=rating_value,
            )
            review.save()
        else:
            book.update_rating(user.pk, rating_value)
        book.update_rating(user.pk,int(rating_value))
        return redirect(request.get_full_path())
    
    # If the user is authenticated, check if the book is already in their favorites
    if user.is_authenticated:
        favorites = user.favorites or {}
        book_favorites = favorites.get("book", [])
        favorited = any(str(fav.get('id')) == str(book.book_id) for fav in book_favorites)
        
    reviews_for_books = Reviews.objects.filter(review_content_type=book_ct,review_content_id=book.book_id)        
    user_current_rating = book.book_average_rate.get(str(user.pk),0)  
    
    # Query for related books with the same genre, excluding the current book,
    # and randomly order them; select up to 10 related books.
    related_books = Books.objects.filter(book_genre=book.book_genre).exclude(book_id=book.book_id).order_by('?')[:10]
       
    context = {
        'book': book,
        'reviews_books' : reviews_for_books,
        'user_current_rating' : user_current_rating,
        'favorited': favorited,
        'related_books': related_books,
    }
    return render(request, 'book/bookdetail.html', context)


@login_required  # Ensure the user is logged in before accessing this view.
@require_POST    # Only allow POST requests for this view.
def bookdetailAddFavoriteView(request, book_id):
    
    # Retrieve the 'category' and 'item_id' parameters from the POST data.
    category = request.POST.get('category')
    item_id = request.POST.get('item_id')
    book = get_object_or_404(Books, book_id=book_id)
    favorited = False
    
    favorites = request.user.favorites or {}
    book_favorites = favorites.get("book", [])
    
    favorited = any(str(fav.get('id')) == str(book.book_id) for fav in book_favorites)
    
     # If either the category or item_id is missing, return a JSON error response.
    if not category or not item_id:
        return JsonResponse({'success': False, 'message': 'Missing parameters.'})
    try:
        if(favorited):
            request.user.remove_favorite('book', book_id)
            action = 'removed'
        else:
            request.user.add_favorite('book', book_id)
            action = 'added'
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
    # Return a JSON response indicating the success of the operation and the action taken.
    return JsonResponse({'success': True, 'action':action})
