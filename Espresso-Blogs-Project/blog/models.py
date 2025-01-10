from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager

# Custom Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

# Models
class Post(models.Model):

    objects = models.Manager() # The default manager
    published = PublishedManager() # custom manager
    tags = TaggableManager(blank=True) # Tagging manager - provided by the taggit package
    class Meta:
        ordering = ['-publish', ]
        indexes = [ models.Index(fields=['-publish']), ]
    
    class Status(models.TextChoices):
        DRAFT = ('DF', 'Draft')
        PUBLISHED = ('PB', 'Published')

    title = models.CharField(max_length=250)
    # the slug field is now required to be unique for the date stored in the publish field.
    slug  = models.SlugField(max_length=250, unique_for_date='publish')
    body  = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    author = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='blog_posts'
    )

    def __str__(self):
        return self.title
    
    # SEO friendly urls for each post
    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                        args=[ self.publish.year, 
                               self.publish.month, 
                               self.publish.day, 
                               self.slug
                             ],
                      )

class Comment(models.Model):
    post = models.ForeignKey(Post, 
                             on_delete=models.CASCADE, 
                             related_name='comments'
                            )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created',]
        indexes = [ models.Index(fields=['created']), ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

