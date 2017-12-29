from django.contrib import admin
from forum.models import Board, Post, Comment, Reply

# Register your models here.
admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
