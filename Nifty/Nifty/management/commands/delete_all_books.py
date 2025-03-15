from django.core.management.base import BaseCommand
from allModels.models import Books

class Command(BaseCommand):
    help = '删除 Books 模型中所有记录及其封面图片'

    def handle(self, *args, **options):
        books = Books.objects.all()
        count = books.count()
        for book in books:
            # 如果存在封面图片，先删除文件
            if book.book_cover_image:
                book.book_cover_image.delete(save=False)
            # 删除数据库记录
            book.delete()
        self.stdout.write(self.style.SUCCESS(f"共删除了 {count} 条记录及其封面图片。"))
