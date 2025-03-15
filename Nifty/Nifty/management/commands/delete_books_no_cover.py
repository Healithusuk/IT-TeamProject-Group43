from django.core.management.base import BaseCommand
from allModels.models import Books

class Command(BaseCommand):
    help = '删除 Books 模型中没有封面的记录'

    def handle(self, *args, **options):
        # 筛选出没有封面图片的记录：movie_cover_image 为 None 或者为空字符串
        qs = Books.objects.filter(book_cover_image__in=[None, ''])
        count = qs.count()
        # 直接删除筛选出的记录
        qs.delete()
        self.stdout.write(self.style.SUCCESS(f"共删除了 {count} 条没有封面的记录。"))