from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from allModels.models import Reviews,Movies,TvShows,Books,ArtworkType

class IndexView(TemplateView):
    # Specify the template to be used for rendering the index page.
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user using the provided credentials.
        user = authenticate(request, username=username, password=password)
        if user is not None:
             # If authentication is successful, log the user in.
            login(request, user)
            return redirect('index')
        else:
            # If authentication fails, get the default context data.
            context = self.get_context_data()
            context['error'] = "Invalid username or password. Please try again."
            return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        # Get the default context data from the parent class.
        context = super().get_context_data(**kwargs)
        
        # Retrieve a random selection of 16 TV shows.
        all_series = list(TvShows.objects.order_by('?')[:16])
        
        # Calculate the midpoint to divide the TV shows into two groups.
        half_series = len(all_series)//2
        
        # Get the artwork type objects for movies and books.
        movie_ct = ArtworkType.objects.get(artwork_type="movie")
        book_ct = ArtworkType.objects.get(artwork_type="book")
        
        # Filter reviews for movies and books based on their content type.
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
