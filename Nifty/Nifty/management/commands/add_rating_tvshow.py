import random
from django.core.management.base import BaseCommand
from allModels.models import TvShows, Accounts

class Command(BaseCommand):
    help = "随机选择用户1或用户2给所有电视剧打分，评分随机在1到5之间"

    def handle(self, *args, **options):
        # 获取两个测试用户，假设他们的 pk 分别为 1 和 2
        try:
            user = Accounts.objects.order_by('?').first()
        except Accounts.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f"用户不存在：{e}"))
            return

        tvshows = TvShows.objects.all()
        
        # 外层循环50次
        for iteration in range(50):
            self.stdout.write(self.style.NOTICE(f"Iteration {iteration + 1}:"))
            # 遍历所有电视剧，为每个电视剧打一个随机分数
            for tvshow in tvshows:
                rating_value = random.randint(1, 5)  # 随机生成1~5之间的整数
                tvshow.update_rating(user.id, rating_value)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"电视剧 {tvshow.tvshow_name} 由用户 {user.username} 打分: {rating_value}"
                    )
                )
        self.stdout.write(self.style.SUCCESS("所有电视剧评分50次已更新。"))

