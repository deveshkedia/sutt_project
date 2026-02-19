from django.db import models
from martor.models import MartorField


# Create your models here.
class Course(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField()
  department = models.CharField(max_length=100)
  
  def __str__(self):
    return self.name
  
class Category(models.Model):
  name = models.CharField(max_length=100)
  
  def __str__(self):
    return self.name
  
class Thread(models.Model):
  title = models.CharField(max_length=200)
  content = MartorField()
  author = models.ForeignKey('auth.User', on_delete=models.SET_NULL,null=True)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
  locked = models.BooleanField(default=False)
  likes_count = models.PositiveIntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  tags = models.ManyToManyField('Tags', blank=True)
  
  def __str__(self):
    return self.title
  
class Replies(models.Model):
  thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
  content = models.TextField()
  author = models.ForeignKey('auth.User', on_delete=models.SET_NULL,null=True)
  is_deleted = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"Reply by {self.author.username} on {self.thread.title}"
  
class Likes(models.Model):
  thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
  user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    unique_together = ('thread', 'user')
    
class Tags(models.Model):
  name = models.CharField(max_length=50, unique=True)
  
  def __str__(self):
    return self.name
    
class Report(models.Model):
  REASON_CHOICES = [
    ('spam', 'Spam'),
    ('inappropriate', 'Inappropriate Content'),
    ('harassment', 'Harassment'),
    ('misinformation', 'Misinformation'),
    ('copyright', 'Copyright Violation'),
    ('other', 'Other'),
  ]
  
  STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('reviewed', 'Reviewed'),
    ('resolved', 'Resolved'),
  ]
  
  thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='reports')
  reporter = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
  reason = models.CharField(max_length=50, choices=REASON_CHOICES)
  description = models.TextField()
  status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"Report on {self.thread.title} by {self.reporter.username}"
  
  class Meta:
    unique_together = ('thread', 'reporter')

class ThreadResource(models.Model):
  FILE_TYPE_CHOICES = [
    ('pdf', 'PDF'),
    ('document', 'Document'),
    ('image', 'Image'),
    ('video', 'Video'),
    ('audio', 'Audio'),
    ('other', 'Other'),
  ]
  
  thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_resources')
  title = models.CharField(max_length=200)
  file = models.FileField(upload_to='thread_resources/%Y/%m/%d/')
  file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES, default='other')
  uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
  description = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.title} - {self.thread.title}"
  
  class Meta:
    ordering = ['-created_at']
