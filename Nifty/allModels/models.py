# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from collections import OrderedDict

def user_avatar_upload_to(instance, filename):
        # 获取原文件扩展名
        ext = filename.split('.')[-1]
        # 如果实例已经有主键，则用该主键作为文件名
        if instance.pk:
            new_filename = f"avatar_{instance.pk}.{ext}"
        else:
            # 如果还没有主键，可以用原始文件名或者用其他方式生成唯一文件名
            new_filename = f"avatar_temp.{ext}"
        return os.path.join('user_avatar', new_filename)  # 文件将保存在 MEDIA_ROOT/user/ 下

def default_favorites():
    return {"movie": [], "book": [], "tv": []}

class Accounts(AbstractUser):
    username = models.CharField(
        max_length=25,  # 修改为25
        unique=True,
        help_text='Required. 25 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    birthday = models.DateField(blank=True, null=True)
    bio = models.CharField(max_length=254,blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_upload_to, blank=True, null=True, default='user_avatar/avatar_default.png')  
    favorites = models.JSONField(default=default_favorites, blank=True)
    following = models.JSONField(default=dict, blank=True)
    follower = models.JSONField(default=dict, blank=True)
    
    @property
    def get_following_num(self):
        return len(self.following or {})
    
    @property
    def get_follower_num(self):
        return len(self.follower or {})
    
    def add_favorite(self, category_key, favorite_item_id):
        # 构造收藏项信息
        favorite_item_id_map = {
            'id': favorite_item_id,         # 作品的主键
        }
        # 确保 favorites 是字典且含有各类别的列表
        if not self.favorites or not isinstance(self.favorites, dict):
            self.favorites = {"movie": [], "book": [], "tv": []}
        if favorite_item_id_map in self.favorites.get(category_key, []):
        # 如果存在，则直接返回，不添加
            return
        # 将新收藏项追加到对应类别的列表中
        self.favorites[category_key].append(favorite_item_id_map)
        self.save()
        
    def remove_favorite(self, category_key, favorite_item_id):
        if not self.favorites or not isinstance(self.favorites, dict):
            self.favorites = {"movie": [], "book": [], "tv": []}
        try:
            favorite_item_id_num = int(favorite_item_id)
            favorite_item_to_remove = {
            'id': favorite_item_id_num,
            }
            self.favorites[category_key].remove(favorite_item_to_remove)
            self.save()
        except ValueError as e:
            print(e)

    
    class Meta:
        db_table = 'Accounts'
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        
    def __str__(self):
        return f'{self.username}[{self.is_superuser}|{self.pk}|{self.email}]'
    
class ArtworkType(models.Model):
    artwork_type_id = models.AutoField(primary_key=True)
    artwork_type = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'Artwork_Type'
        verbose_name = 'Artwork Type'
        verbose_name_plural = 'Artwork Types'
        
    def __str__(self):
        return self.artwork_type
   
class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_text = models.TextField(default=1)
    review_content_type = models.ForeignKey(ArtworkType, models.DO_NOTHING)
    review_content_id = models.IntegerField(default=1)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def remove_reviews(self):
        self.delete()
    
    def get_artwork_name(self):
        """
        根据 review_content_type 和 review_content_id 获取对应的作品对象
        """
        # 获取 ArtworkType 中存储的类别名称，并转换成小写以便比较
        artwork_category = self.review_content_type.artwork_type.lower()
        try:
            if artwork_category == 'movie':
                return Movies.objects.get(movie_id=self.review_content_id).movie_name
            elif artwork_category == 'book':
                return Books.objects.get(book_id=self.review_content_id).book_name
            elif artwork_category == 'tv':
                return TvShows.objects.get(tvshow_id=self.review_content_id).tvshow_name
        except ObjectDoesNotExist:
            return None

    def get_artwork_cover(self):
        artwork_category = self.review_content_type.artwork_type.lower()
        try:
            if artwork_category == 'movie':
                return Movies.objects.get(movie_id=self.review_content_id).movie_cover_image
            elif artwork_category == 'book':
                return Books.objects.get(book_id=self.review_content_id).book_cover_image
            elif artwork_category == 'tv':
                return TvShows.objects.get(tvshow_id=self.review_content_id).tvshow_cover_image
        except ObjectDoesNotExist:
            return None
    
    @property
    def review_content_name(self):
        """
        返回对应作品的名称
        """
        artwork = self.get_artwork_name()
        if artwork:
            return artwork  # 假设各模型都有 artwork_name 属性
        return "Unknown"
    
    @property
    def review_content_cover_image(self):
        """
        返回对应作品的名称
        """
        artwork_cover_image = self.get_artwork_cover()
        if artwork_cover_image:
            return artwork_cover_image  # 假设各模型都有 artwork_name 属性
    
    class Meta:
        db_table = 'Reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        
    def __str__(self):
        return f'{self.review_id}[{self.get_artwork_name()}|{self.pk}|{self.user}]'
    
class Movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=255)
    movie_release_year = models.DateField(null=True, blank=True)
    movie_genre = models.CharField(max_length=255)
    type = models.ForeignKey(ArtworkType, models.DO_NOTHING)
    movie_description = models.TextField()
    movie_director = models.CharField(max_length=255)
    movie_actors = models.TextField()
    movie_country = models.CharField(max_length=255)
    movie_runtime = models.IntegerField()
    movie_imdb = models.CharField(max_length=255,null=True, blank=True)
    movie_cover_image = models.ImageField(upload_to='images/', blank=True, null=True)
    movie_rating_count = models.PositiveIntegerField(default=0)
    movie_average_rate = models.JSONField(default=dict, blank=True)
    
    @property
    def artwork_name(self):
        return self.movie_name
    
    @property
    def star_distribution(self):
        # 初始化统计字典
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        ratings = list(self.movie_average_rate.values())
        total = len(ratings)
        if total == 0:
            return distribution  # 没有评分时，全部为0%
        # 统计每个星级的次数
        for rating in ratings:
            try:
                # 如果 rating 是字符串，也转换为 int
                star = int(rating)
            except (ValueError, TypeError):
                continue
            # 确保范围在 1~5
            star = max(1, min(star, 5))
            distribution[star] += 1
        # 将次数转换为百分比
        for star in distribution:
            distribution[star] = round((distribution[star] / total) * 100, 1)
        # 按 key 从大到小排序
        sorted_distribution = OrderedDict(sorted(distribution.items(), key=lambda x: x[0], reverse=True))
        return sorted_distribution
    
    def update_rating(self, user_id, rating_value):
        # 将用户的评分存入字典中，注意 rating_value 应该在 1 到 5 范围内
        self.movie_average_rate[str(user_id)] = rating_value  # key 转为字符串
        self.movie_rating_count = len(self.movie_average_rate)
        self.save()

    def average_rating(self):
        if self.movie_average_rate:
            try:
                # 将所有评分转换为数字（这里使用 float，确保支持小数评分）
                ratings = [float(v) for v in self.movie_average_rate.values()]
            except (ValueError, TypeError):
                return 0
            count = len(ratings)
            if count > 0:
                return round((sum(ratings) / count) * 2,1)
        return 0
    
    class Meta:
        db_table = 'Movies'
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        
    def __str__(self):
        return f'{self.movie_id}[{self.movie_name}|{self.movie_release_year}|{self.movie_average_rate}]'

class Books(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=255)
    book_release_year = models.DateField(null=True, blank=True)
    book_genre = models.CharField(max_length=255)
    type = models.ForeignKey(ArtworkType, models.DO_NOTHING)
    book_description = models.TextField()
    book_writer = models.CharField(max_length=255)
    book_country = models.CharField(max_length=255)
    book_publisher = models.CharField(max_length=255)
    book_isbn = models.CharField(max_length=255,null=True, blank=True)
    book_cover_image = models.ImageField(upload_to='images/', blank=True, null=True)
    book_rating_count = models.PositiveIntegerField(default=0)
    book_average_rate = models.JSONField(default=dict, blank=True)
    
    @property
    def artwork_name(self):
        return self.book_name
    
    @property
    def star_distribution(self):
        # 初始化统计字典
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        ratings = list(self.book_average_rate.values())
        total = len(ratings)
        if total == 0:
            return distribution  # 没有评分时，全部为0%
        # 统计每个星级的次数
        for rating in ratings:
            try:
                # 如果 rating 是字符串，也转换为 int
                star = int(rating)
            except (ValueError, TypeError):
                continue
            # 确保范围在 1~5
            star = max(1, min(star, 5))
            distribution[star] += 1
        # 将次数转换为百分比
        for star in distribution:
            distribution[star] = round((distribution[star] / total) * 100, 1)
        # 按 key 从大到小排序
        sorted_distribution = OrderedDict(sorted(distribution.items(), key=lambda x: x[0], reverse=True))
        return sorted_distribution
    
    def update_rating(self, user_id, rating_value):
        # 将用户的评分存入字典中，注意 rating_value 应该在 1 到 5 范围内
        self.book_average_rate[str(user_id)] = rating_value  # key 转为字符串
        self.book_rating_count = len(self.book_average_rate)
        self.save()


    def average_rating(self):
        if self.book_average_rate:
            try:
                # 将所有评分转换为数字（这里使用 float，确保支持小数评分）
                ratings = [float(v) for v in self.book_average_rate.values()]
            except (ValueError, TypeError):
                return 0
            count = len(ratings)
            if count > 0:
                return round((sum(ratings) / count) * 2,1)
        return 0
    
    class Meta:
        db_table = 'Books'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        
    def __str__(self):
        return f'{self.book_id}[{self.book_name}|{self.book_release_year}|{self.book_average_rate}]'
    
class TvShows(models.Model):
    tvshow_id = models.AutoField(primary_key=True)
    tvshow_name = models.CharField(max_length=255)
    tvshow_release_year = models.DateField(null=True, blank=True)
    tvshow_genre = models.CharField(max_length=255)
    type = models.ForeignKey(ArtworkType, models.DO_NOTHING)
    tvshow_description = models.TextField()
    tvshow_writer = models.CharField(max_length=255)
    tvshow_country = models.CharField(max_length=255)
    tvshow_publisher = models.CharField(max_length=255)
    tvshow_imdb = models.CharField(max_length=255,null=True, blank=True)
    tvshow_cover_image = models.ImageField(upload_to='images/', blank=True, null=True)
    tvshow_rating_count = models.PositiveIntegerField(default=0)
    tvshow_average_rate = models.JSONField(default=dict, blank=True)
    
    @property
    def artwork_name(self):
        return self.tvshow_name
    
    @property
    def star_distribution(self):
        # 初始化统计字典
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        ratings = list(self.tvshow_average_rate.values())
        total = len(ratings)
        if total == 0:
            return distribution  # 没有评分时，全部为0%
        # 统计每个星级的次数
        for rating in ratings:
            try:
                # 如果 rating 是字符串，也转换为 int
                star = int(rating)
            except (ValueError, TypeError):
                continue
            # 确保范围在 1~5
            star = max(1, min(star, 5))
            distribution[star] += 1
        # 将次数转换为百分比
        for star in distribution:
            distribution[star] = round((distribution[star] / total) * 100, 1)
        # 按 key 从大到小排序
        sorted_distribution = OrderedDict(sorted(distribution.items(), key=lambda x: x[0], reverse=True))
        return sorted_distribution
    
    def update_rating(self, user_id, rating_value):
        # 将用户的评分存入字典中，注意 rating_value 应该在 1 到 5 范围内
        self.tvshow_average_rate[str(user_id)] = rating_value  # key 转为字符串
        self.tvshow_rating_count = len(self.tvshow_average_rate)
        self.save()

    def average_rating(self):
        if self.tvshow_average_rate:
            try:
                # 将所有评分转换为数字（这里使用 float，确保支持小数评分）
                ratings = [float(v) for v in self.tvshow_average_rate.values()]
            except (ValueError, TypeError):
                return 0
            count = len(ratings)
            if count > 0:
                return round((sum(ratings) / count) * 2,1)
        return 0
    
    class Meta:
        db_table = 'TvShows'
        verbose_name = 'TvShow'
        verbose_name_plural = 'TvShows'
        
    def __str__(self):
        return f'{self.tvshow_id}[{self.tvshow_name}|{self.tvshow_release_year}|{self.tvshow_average_rate}]'
    
    
    
