from django.contrib import admin
from forum.models import Class, Question, Answer, Reply

# Register your models here.
admin.site.register(Class)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Reply)
