from django import template, forms


register = template.Library()


@register.filter
def is_file_field(field):
    return type(field.field).__name__ == 'ImageField'


@register.filter
def is_check_box(field):
    return type(field.field).__name__ == 'BooleanField'
