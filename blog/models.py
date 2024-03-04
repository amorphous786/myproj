from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class PublishedManager(models.Manager):
  def get_queryset(self) -> QuerySet:
    return super().get_queryset() \
                  .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
  class Status(models.TextChoices):
    DRAFT = 'DF','Draft'
    PUBLISHED = 'PB','Published'
  title = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255)
  body = models.TextField()
  published = models.DateTimeField(default = timezone.now)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now = True)
  status = models.CharField(max_length=2,choices=Status.choices, default=Status.DRAFT)
  author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
  objects = models.Manager()
  published_posts = PublishedManager()
  class Meta:
    ordering = ['-published']
    indexes = [
      models.Index(fields=['-published']),
    ]
  def __str__(self):
    return self.title