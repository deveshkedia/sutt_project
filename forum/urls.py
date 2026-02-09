from . import views
from django.urls import path

urlpatterns = [
  path("",views.forum_home, name="forum-home"),
  path("threads/",views.ThreadListView.as_view(), name="thread-list"),
  path("threads/create",views.ThreadView.as_view(), name="thread-create"),
  path("threads/<int:pk>/",views.ThreadDetailView.as_view(), name="thread-detail"),
  path("threads/<int:pk>/like",views.like_thread, name="thread-like"),
  path("threads/<int:thread_id>/reply/",views.reply_to_thread, name="thread-reply"),
  path("replies/<int:reply_id>/reply/delete",views.delete_reply, name="reply-delete"),
]