from . import views
from django.urls import path

urlpatterns = [
  path("",views.forum_home, name="forum-home"),
  path("threads/",views.ThreadListView.as_view(), name="thread-list"),
  path("threads/create",views.ThreadView.as_view(), name="thread-create"),
  path("threads/<int:pk>/",views.ThreadDetailView.as_view(), name="thread-detail"),
  path("threads/<int:pk>/like",views.like_thread, name="thread-like"),
  path("threads/<int:thread_id>/report/",views.report_thread, name="thread-report"),
  path("threads/<int:thread_id>/upload-resource/", views.upload_thread_resource, name="upload-resource"),
  path("resources/<int:resource_id>/delete/", views.delete_thread_resource, name="delete-resource"),
  path("reports/",views.ReportListView.as_view(), name="report-list"),
  path("reports/<int:report_id>/review/",views.review_report, name="report-review"),
  path("reports/<int:report_id>/resolve/",views.resolve_report, name="report-resolve"),
  path("threads/<int:thread_id>/reply/",views.reply_to_thread, name="thread-reply"),
  path("replies/<int:reply_id>/reply/delete",views.delete_reply, name="reply-delete"),
]