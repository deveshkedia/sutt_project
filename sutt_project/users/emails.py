from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags


def send_account_creation_email(user_email, user_name, verification_link):
    subject = "Welcome to the SUTT Forum"
    
    html_message = f"""
    <h2>Welcome to SUTT Forum, {user_name}!</h2>"""
    
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


def send_password_reset_email(user_email, user_name, reset_link):
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
    except Exception as e:
      pass


def send_account_deletion_confirmation(user_email, user_name):
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
    except Exception as e:
      pass


def send_profile_update_confirmation(user_email, user_name, changes_dict):
    subject = "Your profile has been updated - SUTT Forum"
    
    changes_html = "<ul>"
    for key, value in changes_dict.items():
        changes_html += f"<li><strong>{key}:</strong> {value}</li>"
    changes_html += "</ul>"
    
    html_message = f"""
    <h2>Profile Update Confirmation</h2>
    <p>Hi {user_name},</p>
    <p>Your profile has been successfully updated with the following changes:</p>
    {changes_html}
    <p>If you didn't make these changes, please contact our support team immediately.</p>
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

