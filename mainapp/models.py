from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

# Create your models here.


class Profile(models.Model):
    """
    extra fields for User model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=7, choices=(('male', 'male'), ('female', 'female'), ('other', 'other')))
    bio = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=50, blank=True)
    slug = models.SlugField()
    profilepic = models.ImageField(upload_to='profile_picture', blank=True)

    def __str__(self):
        return self.user.username


# create a profile object for user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# create slug field for profile
@receiver(post_save, sender=Profile)
def create_profile_slug(sender, instance, created, **kwargs):
    if created:
        instance.slug = slugify(instance.user.username)
        instance.save()
