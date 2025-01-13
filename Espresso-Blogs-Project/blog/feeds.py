from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy # Used for lazy reverse URL resolution such as in CBVs
from markdown import markdown
from .models import Post

class LatestPostsFeed(Feed):
    title = 'The Espresso Blog'
    link = reverse_lazy('blog:post_list')
    description = 'Latest posts from The Espresso Blog.'
    def items(self):
        return Post.published.all()[:5]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return truncatewords_html(markdown(item.body), 30)
    def item_pubdate(self, item):
        return item.publish
