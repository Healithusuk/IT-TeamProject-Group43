from django.test import TestCase
from allModels.models import Movies, ArtworkType, Accounts
from collections import OrderedDict


# Test Movie Scoring Data Types
class MoviesRatingTestCase(TestCase):
    def setUp(self):
        self.artwork = ArtworkType.objects.create(artwork_type='movie')
        # Create a test movie
        self.movie = Movies.objects.create(
            movie_name='Test Movie',
            movie_release_year='2020-01-01',
            movie_genre='Action',
            type=self.artwork,
            movie_description='Test Description',
            movie_director='Test Director',
            movie_actors='Actor1, Actor2',
            movie_country='USA',
            movie_runtime=120,
            movie_imdb='tt1234567',
        )
        # Create two test users
        self.user1 = Accounts.objects.create_user(username='Nitfy',email='nifty@example.com', password='testpass')
        self.user2 = Accounts.objects.create_user(username='test0',email='test0@example.com', password='testpass')
        
        # Rate the movie separately: 4 for user1 and 5 for user2.
        self.movie.update_rating(self.user1.id, 4)
        self.movie.update_rating(self.user2.id, 5)

    def test_average_rating(self):
        self.movie.refresh_from_db()
        # The average rating should be calculated as (4 + 5) / 2 = 4.5
        self.assertEqual(self.movie.average_rating(), 9.0)

class MoviesModelTestCase(TestCase):
    def setUp(self):
        # Create an ArtworkType instance for movies
        self.artwork_movie = ArtworkType.objects.create(artwork_type="movie")
        # Create a Movies instance with required fields
        self.movie = Movies.objects.create(
            movie_name="Test Movie",
            movie_release_year="2020-01-01",
            movie_genre="Action",
            type=self.artwork_movie,
            movie_description="A test movie.",
            movie_director="Test Director",
            movie_actors="Actor1, Actor2",
            movie_country="USA",
            movie_runtime=120,
            movie_imdb="8.0"
        )

    def test_update_rating_and_average_rating(self):
        """
        Test that updating the movie's rating correctly stores the rating,
        updates the rating count, and calculates the overall average rating.
        """
        # Update ratings for two different user IDs
        self.movie.update_rating(user_id=1, rating_value=4)
        self.movie.update_rating(user_id=2, rating_value=5)
        # Refresh the movie object from the database
        self.movie.refresh_from_db()
        
        # Check that the movie_rating_count equals 2
        self.assertEqual(self.movie.movie_rating_count, 2)
        # Calculate expected average rating:
        # Average = (4 + 5) / 2 = 4.5, then multiplied by 2 gives 9.0
        self.assertEqual(self.movie.average_rating(), 9.0)

    def test_star_distribution(self):
        """
        Test that the star_distribution property returns the correct percentage
        distribution based on the stored ratings.
        """
        # Update ratings for two users
        self.movie.update_rating(user_id=1, rating_value=4)
        self.movie.update_rating(user_id=2, rating_value=5)
        self.movie.refresh_from_db()

        # Expect one 4-star rating and one 5-star rating among two ratings:
        # Each should represent 50.0% of the total.
        expected_distribution = OrderedDict([
            (5, 50.0),
            (4, 50.0),
            (3, 0.0),
            (2, 0.0),
            (1, 0.0)
        ])
        self.assertEqual(self.movie.star_distribution, expected_distribution)

    def test_artwork_name_property(self):
        """
        Test that the artwork_name property returns the movie's name.
        """
        self.assertEqual(self.movie.artwork_name, "Test Movie")

    def test_str_method(self):
        """
        Test the __str__ method of the Movies model.
        """
        string_repr = str(self.movie)
        self.assertIn("Test Movie", string_repr)

