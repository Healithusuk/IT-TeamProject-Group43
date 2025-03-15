import datetime
from django.core.management.base import BaseCommand
from allModels.models import Movies

class Command(BaseCommand):
    help = '删除上映日期早于2000年1月1日的电影数据及封面图片'

    def handle(self, *args, **options):
        # 设定截止日期（2000年1月1日之前的电影）
        cutoff_date = datetime.date(2000, 1, 1)

        # 查询所有上映日期早于 cutoff_date 的电影记录
        movies_to_delete = Movies.objects.filter(movie_release_year__lt=cutoff_date)
        count = movies_to_delete.count()

        for movie in movies_to_delete:
            # 如果电影有封面图片，先删除封面图片文件
            if movie.movie_cover_image:
                movie.movie_cover_image.delete(save=False)
            # 删除数据库记录
            movie.delete()

        self.stdout.write(self.style.SUCCESS(f"共删除了 {count} 条记录及其封面图片。"))

