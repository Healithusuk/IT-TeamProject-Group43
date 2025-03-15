import random
from django.core.management.base import BaseCommand
from allModels.models import Books, Accounts

class Command(BaseCommand):
    help = "随机选择用户1或用户2给所有书籍打分，评分随机在1到5之间"

    def handle(self, *args, **options):
        # 获取两个测试用户，假设他们的 pk 分别为 1 和 2
        try:
            user1 = Accounts.objects.get(pk=1)
            user2 = Accounts.objects.get(pk=2)
        except Accounts.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f"用户不存在：{e}"))
            return

        users = [user1, user2]
        books = Books.objects.all()
        
        # 遍历所有电影，为每个电影随机选择一个用户和一个评分
        for book in books:
            chosen_user = random.choice(users)
            rating_value = random.randint(1, 5)  # 随机生成1~5之间的整数
            book.update_rating(chosen_user.id, rating_value)
            self.stdout.write(
                self.style.SUCCESS(
                    f"书籍 {book.book_name} 由用户 {chosen_user.username} 打分: {rating_value}"
                )
            )
        
        self.stdout.write(self.style.SUCCESS("所有书籍评分已更新。"))

