from django.contrib import admin
from forum.models import Class, Post, Comment, Reply

# Register your models here.
admin.site.register(Class)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
