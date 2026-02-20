import asyncio
import os
import sys
import django
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(env_path)

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sutt_project.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import sync_to_async

def send_demo_email():
    """Send a simple demo email using Gmail credentials"""
    try:
        result = send_mail(
            subject="Demo Email from Django",
            message="This is a demo email sent from Django using Gmail SMTP!",
            from_email=os.getenv('EMAIL_HOST_USER'),
            recipient_list=["f20250803@pilani.bits-pilani.ac.in"],
            fail_silently=False,
        )
        print(f"✅ Email sent successfully! ({result} message sent)")
        return result
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return None

@sync_to_async
def send_async_email():
    return send_mail(
        subject="Async Email Test",
        message="This email is sent asynchronously with Django 4.x.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["deveshkedia.official@gmail.com"],
    )

# Send demo email
if __name__ == "__main__":
    print("🚀 Sending demo email...")
    send_demo_email()