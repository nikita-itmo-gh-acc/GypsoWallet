from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo = models.ImageField(blank=True)
    reg_date = models.DateTimeField(auto_now_add=True)
    balance = models.IntegerField(default=500)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return self.user.name


class Token(models.Model):
    name = models.CharField(max_length=255)
    count = models.FloatField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
