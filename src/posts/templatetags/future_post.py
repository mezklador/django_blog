from django.utils import timezone
from django import template

register = template.Library()

@register.filter(name="future_post")
def future_post(modelentry):
    return modelentry > timezone.now().date()
