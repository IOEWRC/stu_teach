from django import template
from forum.models import Class


register = template.Library()


@register.filter
def user_is_teacher(user, class_pk):
    return user == Class.objects.get(pk=class_pk).created_by
