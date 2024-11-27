from django import template

register = template.Library()

# untuk navbar diatas biar sesuai per user nya
@register.filter
def in_list(value, the_list):
    return value in the_list
