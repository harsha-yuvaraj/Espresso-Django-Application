from django import template
from ..models import Post

# This variable will be used to register the template tags and filters of the application.
register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()




