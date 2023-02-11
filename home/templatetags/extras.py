from django import template

register = template.Library()

@register.filter(name='get_val')
def get_val(dict_, key):
    return dict_.get(key)