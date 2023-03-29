from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published') # own manager for filtering - published posts


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250) # post's title - CharField = VARCHAR
    slug = models.SlugField(max_length=250, unique_for_date='publish') # label to build SEO (search engine optimization - urls for posts)
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE) # Foreign Key
    body = models.TextField() # content of the post - TextField = TEXT in SQL
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) # automatically inserts current time
    updated = models.DateTimeField(auto_now=True) # automatically updates with current time
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    
    objects = models.Manager() # returns all posts - Post.objects.filter()
    published = PublishedManager() # returns published posts defined in class PublishedManager - Post.published.filter()
    
    class Meta: # it contains metadata - data sorted in descending order (because of '-') according to 'publish' column
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse ('blog:post_detail',
                        args=[self.publish.year,
                              self.publish.month,
                              self.publish.day,
                              self.slug])