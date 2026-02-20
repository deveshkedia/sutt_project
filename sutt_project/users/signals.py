from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from users.emails import send_account_creation_email
import os


@receiver(post_save, sender=User)
def send_welcome_email_on_signup(sender, instance, created, **kwargs):
    if created and instance.email:
        try:
            send_account_creation_email(
                user_email=instance.email,
                user_name=instance.get_full_name() or instance.username,
            )
        except Exception as e:
          pass