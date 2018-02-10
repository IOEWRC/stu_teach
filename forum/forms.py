from .models import Class, Question, Answer, Reply
from django.forms import ModelForm


class ClassCreateForm(ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'description', 'class_avatar', ]


class QuestionCreateForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'instruction', 'files', ]


class AnswerCreateForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['body', 'files']


class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body',]


