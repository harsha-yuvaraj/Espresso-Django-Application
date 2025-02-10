from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown
import datetime
from ..models import Post

# This variable will be used to register the template tags and filters of the application.
register = template.Library()

@register.simple_tag
def total_posts():
    # returns a value indicating the total number of published posts
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    # returns a queryset of posts with the total number of comments for each post.
    return Post.published.annotate(total_comments=Count('comments')).filter(total_comments__gt=0).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown(text))

@register.filter(name='time_ago')
def time_ago(published_date):
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now - published_date
    seconds = diff.total_seconds()

    if seconds < 60:
        return "now"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif seconds < 2592000:  # 30 days
        days = int(seconds // 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif seconds < 31536000:  # 12 months ~ 365 days
        months = int(seconds // 2592000)
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = int(seconds // 31536000) 
        return f"{years} year{'s' if years > 1 else ''} ago"
    