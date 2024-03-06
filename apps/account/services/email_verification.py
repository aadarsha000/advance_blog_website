from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    subject = "Verify your email"
    message = f"Your OTP is {token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
