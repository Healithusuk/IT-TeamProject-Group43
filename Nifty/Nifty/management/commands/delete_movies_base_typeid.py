from django.core.management.base import BaseCommand
from allModels.models import Movies

class Command(BaseCommand):
    help = '删除 type_id 不为 1 的电影记录及其封面图片'

    def handle(self, *args, **options):
        # 查询所有 type_id 不为 1 的电影记录
        movies_to_delete = Movies.objects.exclude(type_id=1)
        count = movies_to_delete.count()

        for movie in movies_to_delete:
            # 如果存在封面图片，则删除对应的文件
            if movie.movie_cover_image:
                movie.movie_cover_image.delete(save=False)
            # 删除数据库记录
            movie.delete()

        self.stdout.write(self.style.SUCCESS(f"共删除了 {count} 条记录及其封面图片。"))
