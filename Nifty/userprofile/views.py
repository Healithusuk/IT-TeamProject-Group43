from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from allModels.models import Movies, Books, TvShows, Reviews, Accounts  # 根据实际 app 名称调整导入路径
from .forms import AccountSettingsForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='index')  # 如果只有登录用户才能访问
def profileView(request, user_id):
    
    # 假设当前用户已登录
    profile_user = get_object_or_404(Accounts, pk=user_id)
    is_owner = (request.user.id == profile_user.id)
    is_followed = False
    # 处理更新个人信息
    if request.method == "POST":
        form = AccountSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.id)  # 或其他你希望重定向的页面
    else:
        form = AccountSettingsForm(instance=request.user)

    # favorites 字段结构: {"movie": [{id:.., name:..}, ...], "book": [...], "tv": [...]}
    favorites_data = profile_user.favorites or {"movie": [], "book": [], "tv": []}

    favorite_details = {"movie": [], "book": [], "tv": []}

    # 处理电影收藏
    for item in favorites_data.get("movie", []):
        # 查询电影对象（这里使用 get_object_or_404 或 get() 均可）
        movie = get_object_or_404(Movies, movie_id=item['id'])
        favorite_details["movie"].append({
            "self":movie,
            "name": movie.movie_name,
            "cover": movie.movie_cover_image.url if movie.movie_cover_image else None
        })

    # 处理书籍收藏
    for item in favorites_data.get("book", []):
        book = get_object_or_404(Books, book_id=item['id'])
        favorite_details["book"].append({
            "self":book,
            "name": book.book_name,
            "cover": book.book_cover_image.url if book.book_cover_image else None
        })

    # 处理电视收藏
    for item in favorites_data.get("tv", []):
        tv = get_object_or_404(TvShows, tvshow_id=item['id'])
        favorite_details["tv"].append({
            "self":tv,
            "name": tv.tvshow_name,
            "cover": tv.tvshow_cover_image.url if tv.tvshow_cover_image else None
        })
    
    # 过滤出当前登录用户的所有评论
    user_reviews = Reviews.objects.filter(user=profile_user)
    
    user_following_num = profile_user.get_following_num
    user_follower_num = profile_user.get_follower_num
    
    if not is_owner and str(user_id) in request.user.following:
         is_followed = True
             
    
    context = {
        'profile_user': profile_user,
        'form': form,
        'favorites': favorite_details,
        'reviews': user_reviews,
        'user_following_num': user_following_num,
        'user_follower_num': user_follower_num,
        'is_followed': is_followed,
        
    }
    if is_owner:
        return render(request, 'userprofile/userprofile.html', context)
    else:
        return render(request, 'userprofile/guestprofile.html', context)

@login_required
@require_POST
def deleteFavorite(request, user_id):
    category = request.POST.get('category')
    item_id  = request.POST.get('item_self')
    try:
        print("1")
        request.user.remove_favorite(category, item_id)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': True})

@login_required
@require_POST
def deleteReview(request, user_id):
    review_id = request.POST.get('review_id')
    if not review_id:
        return JsonResponse({'success': False, 'message': 'Missing review id'})
    try:
        review = Reviews.objects.get(pk=review_id, user=request.user)
        review.remove_reviews()
        return JsonResponse({'success': True})
    except Reviews.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Review not found'})
    
@login_required
@require_POST
def followUser(request, user_id):
    if not user_id:
        return JsonResponse({"success": False, "message": "Missing target user id."}, status=400)
    
    try:
        target_user_id = int(user_id)
        target_user = Accounts.objects.get(pk=target_user_id)
    except (ValueError, Accounts.DoesNotExist):
        return JsonResponse({"success": False, "message": "Target user not found."}, status=404)
    
    current_user = request.user

    # 确保 following 和 follower 是字典
    if not current_user.following or not isinstance(current_user.following, dict):
        current_user.following = {}
    if not target_user.follower or not isinstance(target_user.follower, dict):
        target_user.follower = {}

    # 如果当前用户还没有关注目标用户，则添加关注
    if str(target_user.id) not in current_user.following:
        current_user.following[str(target_user.id)] = True
        current_user.save()
        action = 'followed'
    else:
        current_user.following.pop(str(target_user.id), None)
        current_user.save()
        action = 'unfollowed'
        
    
    # 同时在目标用户的 follower 字段中添加当前用户
    if str(current_user.id) not in target_user.follower:
        target_user.follower[str(current_user.id)] = True
        target_user.save()
        action = 'followed'
    else:
        target_user.follower.pop(str(current_user.id), None)
        target_user.save()
        action = 'unfollowed'
    
    user_follower_num = len(target_user.follower.keys())

    return JsonResponse({'success': True, 'action':action, 'user_follower_num': user_follower_num,})

def followDetail(request, user_id):
    # 获取要查看的用户对象
    profile_user = get_object_or_404(Accounts, pk=user_id)
    
    # 如果 following 存在，则将字典的键转换为整数列表；否则为空列表
    if profile_user.following and isinstance(profile_user.following, dict):
        following_ids = [int(uid) for uid in profile_user.following.keys()]
    else:
        following_ids = []
    
    # 同理，获取 follower 的用户 ID 列表
    if profile_user.follower and isinstance(profile_user.follower, dict):
        follower_ids = [int(uid) for uid in profile_user.follower.keys()]
    else:
        follower_ids = []
    
    # 查询对应的用户对象
    following_users = Accounts.objects.filter(pk__in=following_ids)
    follower_users = Accounts.objects.filter(pk__in=follower_ids)
    
    context = {
        'profile_user': profile_user,
        'following_users': following_users,
        'follower_users': follower_users,
    }
    return render(request, 'userprofile/followdetail.html', context)