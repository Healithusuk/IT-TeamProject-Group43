from django.test import TestCase
from django.contrib.auth import get_user_model
from allModels.models import Movies, ArtworkType, Accounts

User = get_user_model()

class MoviesRatingTestCase(TestCase):
    def setUp(self):
        # 创建一个 ArtworkType 实例
        self.artwork = ArtworkType.objects.create(artwork_type='movie')
        
        # 创建一个测试电影
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
        
        # 创建两个测试用户
        self.user1 = Accounts.objects.create_user(username='Nitfy', password='testpass')
        self.user2 = Accounts.objects.create_user(username='test0', password='testpass')
        
        # 分别给电影打分：user1 给 4 分，user2 给 5 分
        self.movie.update_rating(self.user1.id, 4)
        self.movie.update_rating(self.user2.id, 5)

    def test_average_rating(self):
        # 刷新 movie 对象数据
        self.movie.refresh_from_db()
        # 计算平均评分应为 (4 + 5) / 2 = 4.5
        self.assertEqual(self.movie.average_rating, 4.5)
