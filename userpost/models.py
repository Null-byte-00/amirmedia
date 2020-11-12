from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    picture = models.ImageField(null=True, blank=True, upload_to='post_picture')
    text = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    tags = TaggableManager(blank=True)

    def __str__(self):
        return f'{self.user.username}:{self.title[:20]} ...'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}:{self.text} ...'


@receiver(post_save, sender=Post)
def create_post_slug(sender, instance, created, **kwargs):
    if created:
        instance.slug = slugify(instance.title)
        instance.save()
