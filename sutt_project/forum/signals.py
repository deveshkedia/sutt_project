from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from forum.models import Replies, Report, Thread
from forum.emails import (
    send_thread_reply_notification,
    send_report_notification,
    send_data_to_admin,
)


@receiver(post_save, sender=Replies)
def notify_thread_author_on_reply(sender, instance, created, **kwargs):
    if created and instance.thread.author:
        try:
            send_thread_reply_notification(
                thread_author_email=instance.thread.author.email,
                reply_author_name=instance.author.get_full_name() or instance.author.username,
                thread_title=instance.thread.title
            )
        except Exception as e:
          pass


@receiver(post_save, sender=Report)
def notify_thread_author_on_report(sender, instance, created, **kwargs):
    if created and instance.thread.author:
        try:
            send_report_notification(
                thread_author_email=instance.thread.author.email,
                reporter_name=instance.reporter.get_full_name() or instance.reporter.username,
                thread_title=instance.thread.title,
                report_reason=instance.get_reason_display()
            )
        except Exception as e:
          pass
    
    if created:
        try:
            moderators = instance.thread.author.groups.filter(name='Moderator')
            if moderators.exists():
                admin_emails = [user.email for user in moderators.user_set.all() if user.email]
                if admin_emails:
                    send_data_to_admin(
                        admin_email=admin_emails[0], 
                        subject_line=f"New Report: {instance.thread.title}",
                        message_content=f"A report has been submitted for the thread by {instance.thread.author.username}",
                        data_dict={
                            "Thread": instance.thread.title,
                            "Reason": instance.get_reason_display(),
                            "Reporter": instance.reporter.username,
                            "Description": instance.description[:100] + "..."
                        }
                    )
        except Exception as e:
          pass 
