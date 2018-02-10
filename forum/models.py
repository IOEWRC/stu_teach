from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from .random_class_code import random_string_generator


class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_set')
    created_at = models.DateTimeField(auto_now_add=True)
    class_avatar = models.ImageField(upload_to='class_image', blank=True)
    students = models.ManyToManyField(User, related_name='class_student')
    code = models.CharField(max_length=12, blank=True)

    def get_absolute_url(self):
        return reverse('forum:class_list')

    def __str__(self):
        return self.name


@receiver(post_save, sender=Class)
def save_class_code(sender, **kwargs):
    if kwargs['created']:
        code = random_string_generator()
        class_object = Class.objects.get(pk=kwargs['instance'].pk)
        qs_exists = Class.objects.filter(code=code).exists()
        if qs_exists:
            code = random_string_generator()
            return save_class_code(sender, **kwargs)
        class_object.code = code
        class_object.save()


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
    files = models.FileField(upload_to='question_files', blank=True)

    def get_absolute_url(self):
        return reverse('forum:class_detail', kwargs={'pk': self.class_room.pk})  # TODO use question detail view

    def __str__(self):
        return self.title


class Answer(models.Model):
    body = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_set')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(User, related_name='answer_upvoted')
    downvoted_by = models.ManyToManyField(User, related_name='answer_downvoted')
    files = models.FileField(upload_to='answer_files', blank=True)

    def get_absolute_url(self):
        return reverse('forum:question_detail', kwargs={'pk': self.question.pk})


class Reply(models.Model):
    body = models.TextField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="reply_set")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reply_set")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    """Reaction todo"""  # TODO

    def get_absolute_url(self):
        return reverse('forum:answer_detail', kwargs={'pk': self.answer.pk})