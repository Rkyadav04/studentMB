import random
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp(user):
    """Send OTP to user's email and mobile"""
    otp = generate_otp()
    profile = Profile.objects.get(user=user)
    profile.otp = otp
    profile.save()

    # Send Email
    subject = "Your StudentMB OTP"
    message = f"Hello {user.username},\n\nYour OTP is: {otp}\n\nThanks,\nStudentMB Team"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    # Send SMS (Here we just print it, integrate an SMS API like Twilio/Fast2SMS)
    print(f"OTP sent to {profile.mobile}: {otp}")
