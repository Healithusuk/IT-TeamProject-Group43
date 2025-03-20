from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = '通过 QQ SMTP 发送一封测试邮件到指定邮箱'

    def add_arguments(self, parser):
        # 添加命令参数，recipient 为必传参数
        parser.add_argument('recipient', type=str, help='接收邮件的邮箱地址')

    def handle(self, *args, **options):
        recipient = options['recipient']
        subject = 'Test Email'
        message = '这是一封通过 Django 管理命令使用 QQ SMTP 发送的测试邮件。'
        from_email = settings.EMAIL_HOST_USER

        # 发送邮件
        send_mail(subject, message, from_email, [recipient], fail_silently=False)

        self.stdout.write(self.style.SUCCESS(f"邮件成功发送到 {recipient}"))

