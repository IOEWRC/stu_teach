from django.contrib import admin
from forum.models import Class, Question, Comment, Reply

# Register your models here.
admin.site.register(Class)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Reply)
