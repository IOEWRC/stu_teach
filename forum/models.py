from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_set')
    created_at = models.DateTimeField(auto_now_add=True)
    class_avatar = models.ImageField(upload_to='class_image', blank=True)
    students = models.ManyToManyField(User, related_name='class_student')

    def get_absolute_url(self):
        return reverse('forum:class_list')

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    instruction = models.TextField()
    class_room = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='question_set')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(User, related_name='question_upvoted')
    downvoted_by = models.ManyToManyField(User, related_name='question_downvoted')

    def get_absolute_url(self):
        return reverse('forum:class_detail', kwargs={'pk': self.class_room.pk})  # TODO use question detail view

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comment_set')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(User, related_name='comment_upvoted')
    downvoted_by = models.ManyToManyField(User, related_name='comment_downvoted')


class Reply(models.Model):
    body = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reply_set")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reply_set")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    """Reaction todo"""  # TODO
