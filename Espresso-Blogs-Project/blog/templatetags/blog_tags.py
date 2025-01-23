from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown
from ..models import Post

# This variable will be used to register the template tags and filters of the application.
register = template.Library()

@register.simple_tag
def total_posts():
    # returns a value indicating the total number of published posts
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=4):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=4):
    # returns a queryset of posts with the total number of comments for each post.
    return Post.published.annotate(total_comments=Count('comments')).filter(total_comments__gt=0).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown(text))