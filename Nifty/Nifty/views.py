from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from allModels.models import Reviews,Movies,TvShows,Books,ArtworkType
from django.contrib.contenttypes.models import ContentType

class IndexView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # 登录失败时，把错误信息加入上下文并重新渲染页面
            context = self.get_context_data()
            context['error'] = "Invalid credentials. Please try again."
            return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 随机抽取 10 条评论
        all_series = list(TvShows.objects.order_by('?')[:16])
        half_series = len(all_series)//2
        movie_ct = ArtworkType.objects.get(artwork_type="movie")
        book_ct = ArtworkType.objects.get(artwork_type="book")
        reviews_for_movies = Reviews.objects.filter(review_content_type=movie_ct)
        reviews_for_books = Reviews.objects.filter(review_content_type=book_ct)        
        
        context['series_left'] = all_series[:half_series]
        context['series_right'] = all_series[half_series:]
        context['books'] = Books.objects.order_by('?')[:8]
        context['movies'] = Movies.objects.order_by('?')[:8]
        context['reviews_movies'] = reviews_for_movies
        context['reviews_books'] = reviews_for_books
        context['movie_count'] = Movies.objects.count()
        context['book_count'] = Books.objects.count() 
        context['tv_count'] = TvShows.objects.count()
        return context
