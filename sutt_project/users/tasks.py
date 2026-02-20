"""
Celery tasks for users app.
Handles async email sending for user account events.
"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_welcome_email_task(self, user_email, user_name, verification_link=None):
    """
    Async task: Send welcome/verification email to new user.
    """
    subject = "Welcome to SUTT Forum!"
    
    if verification_link:
        html_message = f"""
        <h2>Welcome to SUTT Forum, {user_name}!</h2>
        <p>Please verify your email address by clicking the button below:</p>
        <p><a href="{verification_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
            Verify Email
        </a></p>
        <p>Or copy and paste this link in your browser:</p>
        <p>{verification_link}</p>
        <p>This link will expire in 24 hours.</p>
        """
    else:
        html_message = f"""
        <h2>Welcome to SUTT Forum, {user_name}!</h2>
        <p>Thank you for creating an account on our forum.</p>
        <p>You can now:</p>
        <ul>
            <li>Create and participate in discussions</li>
            <li>Reply to threads</li>
            <li>Like and react to posts</li>
            <li>Join our community</li>
        </ul>
        <p>If you have any questions, feel free to reach out to us.</p>
        <p>Happy discussing!</p>
        """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"✅ Welcome email sent to {user_email}")
        return f"Email sent to {user_email}"
    except Exception as exc:
        logger.error(f"❌ Failed to send welcome email: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_password_reset_email_task(self, user_email, user_name, reset_link):
    """
    Async task: Send password reset email to user.
    """
    subject = "Reset your password - SUTT Forum"
    
    html_message = f"""
    <h2>Password Reset Request</h2>
    <p>Hi {user_name},</p>
    <p>We received a request to reset your password. Click the button below to reset it:</p>
    <p><a href="{reset_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
        Reset Password
    </a></p>
    <p>Or copy and paste this link in your browser:</p>
    <p>{reset_link}</p>
    <p>This link will expire in 1 hour.</p>
    <p>If you didn't request this, you can ignore this email. Your password will remain unchanged.</p>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"✅ Password reset email sent to {user_email}")
        return f"Email sent to {user_email}"
    except Exception as exc:
        logger.error(f"❌ Failed to send password reset email: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_account_deletion_confirmation_task(self, user_email, user_name):
    """
    Async task: Send confirmation email that account has been deleted.
    """
    subject = "Your account has been deleted - SUTT Forum"
    
    html_message = f"""
    <h2>Account Deletion Confirmation</h2>
    <p>Hi {user_name},</p>
    <p>Your SUTT Forum account has been successfully deleted.</p>
    <p>All your personal data and posts have been removed from our system.</p>
    <p>If you change your mind, you can create a new account at any time.</p>
    <p>Thank you for being part of our community!</p>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"✅ Account deletion confirmation sent to {user_email}")
        return f"Email sent to {user_email}"
    except Exception as exc:
        logger.error(f"❌ Failed to send account deletion email: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_suspicious_activity_alert_task(self, user_email, user_name, activity_description):
    """
    Async task: Send alert email for suspicious account activity.
    """
    subject = "Suspicious Activity Alert - SUTT Forum"
    
    html_message = f"""
    <h2>Security Alert</h2>
    <p>Hi {user_name},</p>
    <p>We detected suspicious activity on your account:</p>
    <p><strong>{activity_description}</strong></p>
    <p>If this was you, you can ignore this email.</p>
    <p>If you didn't authorize this activity, please change your password immediately.</p>
    <p>If you need help, contact our support team.</p>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"✅ Suspicious activity alert sent to {user_email}")
        return f"Email sent to {user_email}"
    except Exception as exc:
        logger.error(f"❌ Failed to send suspicious activity alert: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)
