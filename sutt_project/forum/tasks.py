"""
Celery tasks for forum app.
Handles async email sending for forum events.
"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_thread_reply_notification_task(self, thread_author_email, reply_author_name, thread_title):
    """
    Async task: Send email notification to thread author when someone replies.
    """
    subject = f"New reply to your thread: {thread_title}"
    
    html_message = f"""
    <h3>You have a new reply!</h3>
    <p><strong>{reply_author_name}</strong> replied to your thread:</p>
    <p><em>"{thread_title}"</em></p>
    <p>Click the link below to view the reply:</p>
    <p><a href="{settings.SITE_URL}/forum">View Thread</a></p>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[thread_author_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"✅ Reply notification sent to {thread_author_email}")
        return f"Email sent to {thread_author_email}"
    except Exception as exc:
        logger.error(f"❌ Failed to send reply notification: {str(exc)}")
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_thread_like_notification_task(self, thread_author_email, liker_name, thread_title):
    """
    Async task: Send email notification when someone likes a thread.
    """
    subject = f"Your thread was liked: {thread_title}"
    
    html_message = f"""
    <h3>Your thread received a like!</h3>
    <p><strong>{liker_name}</strong> liked your thread:</p>
    <p><em>"{thread_title}"</em></p>
    <p><a href="{settings.SITE_URL}/forum">View Thread</a></p>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[thread_author_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"✅ Like notification sent to {thread_author_email}")
        return f"Email sent to {thread_author_email}"
    except Exception as exc:
        logger.error(f"❌ Failed to send like notification: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_report_notification_task(self, thread_author_email, reporter_name, thread_title, report_reason):
    """
    Async task: Send email notification when a thread is reported.
    """
    subject = f"Your thread has been reported: {thread_title}"
    
    html_message = f"""
    <h3>Your thread has been reported</h3>
    <p><strong>{reporter_name}</strong> reported your thread:</p>
    <p><em>"{thread_title}"</em></p>
    <p><strong>Reason:</strong> {report_reason}</p>
    <p>Our moderation team will review this report shortly.</p>
    <p><a href="{settings.SITE_URL}/forum">View Thread</a></p>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[thread_author_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"✅ Report notification sent to {thread_author_email}")
        return f"Email sent to {thread_author_email}"
    except Exception as exc:
        logger.error(f"❌ Failed to send report notification: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_admin_notification_task(self, admin_email, subject_line, message_content, data_dict=None):
    """
    Async task: Send generic admin notification.
    """
    html_message = f"""
    <h3>{subject_line}</h3>
    <p>{message_content}</p>
    """
    
    if data_dict:
        html_message += "<p><strong>Details:</strong></p><ul>"
        for key, value in data_dict.items():
            html_message += f"<li><strong>{key}:</strong> {value}</li>"
        html_message += "</ul>"
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject_line,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[admin_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"✅ Admin notification sent to {admin_email}")
        return f"Email sent to {admin_email}"
    except Exception as exc:
        logger.error(f"❌ Failed to send admin notification: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_welcome_email_task(self, user_email, user_name):
    """
    Async task: Send welcome email to new user.
    """
    subject = "Welcome to SUTT Forum!"
    
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
