import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp(email):
    otp=str(random.randint(100000,999999))

    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}. Please use this to complete your action.',settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return otp

