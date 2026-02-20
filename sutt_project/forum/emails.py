from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_welcome_email(user_email, user_name):
    subject = "Welcome to SUTT Forum!"
    
    context = {
        'user_name': user_name,
        'site_name': 'SUTT Forum',
    }
    
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
    except Exception as e:
      pass

def send_thread_reply_notification(thread_author_email, reply_author_name, thread_title):
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
    except Exception as e:
      pass

def send_thread_like_notification(thread_author_email, liker_name, thread_title):
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
    except Exception as e:
      pass

def send_reply_like_notification(reply_author_email, liker_name, thread_title):
    subject = f"Your reply was liked: {thread_title}"
    
    html_message = f"""
    <h3>Your reply received a like!</h3>
    <p><strong>{liker_name}</strong> liked your reply in:</p>
    <p><em>"{thread_title}"</em></p>
    <p><a href="{settings.SITE_URL}/forum">View Reply</a></p>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[reply_author_email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
      pass

def send_report_notification(thread_author_email, reporter_name, thread_title, report_reason):
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
    except Exception as e:
      pass

def send_data_to_admin(admin_email, subject_line, message_content, data_dict=None):
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
    except Exception as e:
      pass