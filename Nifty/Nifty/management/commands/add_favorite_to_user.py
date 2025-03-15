import random
from django.core.management.base import BaseCommand
from allModels.models import Movies, Books, TvShows, Accounts  # 根据实际 app 名称调整导入路径

class Command(BaseCommand):
    help = '为指定用户添加一个随机收藏作品，从 Movies、Books、TvShows 中随机选取一个'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='需要添加收藏的用户名')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = Accounts.objects.get(username=username)
        except Accounts.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'用户 "{username}" 不存在。'))
            return

        # 定义类别与对应模型的字典
        categories = {
            'movie': Movies,
            'book': Books,
            'tv': TvShows,
        }

        # 随机选择一个类别
        category_key = random.choice(list(categories.keys()))
        model_class = categories[category_key]

        # 随机选取该类别中的一个作品
        instance = model_class.objects.order_by('?').first()
        if not instance:
            self.stdout.write(self.style.WARNING(f'{category_key} 类别中没有作品可选。'))
            return

        # 构造收藏项信息
        favorite_item = {
            'id': instance.pk,         # 作品的主键
        }

        # 确保 favorites 是字典且含有各类别的列表
        if not user.favorites or not isinstance(user.favorites, dict):
            user.favorites = {"movie": [], "book": [], "tv": []}

        # 将新收藏项追加到对应类别的列表中
        user.favorites[category_key].append(favorite_item)
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f'已为用户 "{username}" 添加收藏: {favorite_item} 到类别 "{category_key}"'
        ))
