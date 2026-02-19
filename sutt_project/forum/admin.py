from django.contrib import admin
from django.db import models
from .models import Course, Category, Thread, Replies, Tags, Report, ThreadResource
from martor.widgets import AdminMartorWidget

# Register your models here.

class MardownAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

admin.site.register(Thread, MardownAdmin)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Replies)
admin.site.register(Tags)
admin.site.register(Report)
admin.site.register(ThreadResource)