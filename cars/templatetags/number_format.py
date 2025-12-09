# templatetags/number_format.py
from django import template

register = template.Library()

@register.filter
def thousands_dot(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except:
        return value
