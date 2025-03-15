from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core import mail
from django.conf import settings
from django.core.mail import send_mail

class GmailSMTPTestCase(TestCase):
    def test_send_email_to_specified_email(self):
        recipient = "healithusuk@gmail.com"  # 指定接收邮箱
        subject = "Test Email"
        message = "This is a test email sent via Gmail SMTP."
        from_email = settings.EMAIL_HOST_USER

        # 发送邮件
        send_mail(subject, message, from_email, [recipient], fail_silently=False)

        # 检查邮件队列中是否有一封邮件
        self.assertEqual(len(mail.outbox), 1)

        # 获取发送的邮件并验证相关信息
        email = mail.outbox[0]
        self.assertEqual(email.subject, subject)
        self.assertEqual(email.body, message)
        self.assertEqual(email.from_email, from_email)
        self.assertEqual(email.to, [recipient])

