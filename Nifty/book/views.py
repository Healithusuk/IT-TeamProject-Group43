from django.shortcuts import render, get_object_or_404, redirect
from allModels.models import Books, Reviews, ArtworkType
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def bookhomeView(request):
    query = request.GET.get('q', '')  # 获取关键字，默认为空
    if query:
        books = Books.objects.filter(book_name__icontains=query) 
    else:
        books = Books.objects.none()
        
    context = {
        'query': query,
        'books': books,
    }
    return render(request, 'book/bookhome.html', context)

def bookdetailView(request, book_id):
    
    user = request.user
    book = get_object_or_404(Books, book_id=book_id)
    book_ct = ArtworkType.objects.get(artwork_type="book")
    favorited = False
    
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
    if user.is_authenticated:
        # favorites 存储的是字典，其中 "book" 对应一个列表
        favorites = user.favorites or {}
        book_favorites = favorites.get("book", [])
        favorited = any(str(fav.get('id')) == str(book.book_id) for fav in book_favorites)
        
    reviews_for_books = Reviews.objects.filter(review_content_type=book_ct,review_content_id=book.book_id)        
    user_current_rating = book.book_average_rate.get(str(user.pk),0)  
    
    # 查询相同 genre 的书籍，排除当前这本书，随机取几本，比如取 5 本
    related_books = Books.objects.filter(book_genre=book.book_genre).exclude(book_id=book.book_id).order_by('?')[:10]
       
    context = {
        'book': book,
        'reviews_books' : reviews_for_books,
        'user_current_rating' : user_current_rating,
        'favorited': favorited,
        'related_books': related_books,
    }
    return render(request, 'book/bookdetail.html', context)

@login_required
@require_POST
def bookdetailAddFavoriteView(request, book_id):
    # 获取 POST 数据中的类别和收藏项 ID
    category = request.POST.get('category')
    item_id = request.POST.get('item_id')
    book = get_object_or_404(Books, book_id=book_id)
    favorited = False
    # favorites 存储的是字典，其中 "book" 对应一个列表
    favorites = request.user.favorites or {}
    book_favorites = favorites.get("book", [])
    # 假设你存储时是以字典形式保存，并且 key 为 "id"
    # 转换为字符串，确保匹配
    favorited = any(str(fav.get('id')) == str(book.book_id) for fav in book_favorites)
    
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
    
    return JsonResponse({'success': True, 'action':action})
