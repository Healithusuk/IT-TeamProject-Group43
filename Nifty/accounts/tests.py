from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core import mail
from django.conf import settings
from django.core.mail import send_mail

# Test for SMTP server(Password Reset)
class GmailSMTPTestCase(TestCase):
    def test_send_email_to_specified_email(self):
        recipient = "healithusuk@gmail.com" 
        subject = "Test Email"
        message = "This is a test email sent via Gmail SMTP."
        from_email = settings.EMAIL_HOST_USER

        # send email
        send_mail(subject, message, from_email, [recipient], fail_silently=False)

        # Check if there is an email in the mail queue
        self.assertEqual(len(mail.outbox), 1)

        # Get sent emails and validate the information
        email = mail.outbox[0]
        self.assertEqual(email.subject, subject)
        self.assertEqual(email.body, message)
        self.assertEqual(email.from_email, from_email)
        self.assertEqual(email.to, [recipient])

