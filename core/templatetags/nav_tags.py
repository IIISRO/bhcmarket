from django import template
from product.models import Category

register = template.Library()

@register.simple_tag
def NavCategories():
    categories = Category.objects.filter(parent = None).order_by('created_at')
    return categories