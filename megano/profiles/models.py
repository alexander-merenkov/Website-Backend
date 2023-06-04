from django.db import models
from django.contrib.auth.models import User


def avatar_uploads(instance: User, filename) -> str:
    return 'users/user_{pk}/avatar/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name='name', max_length=100, unique=True)
    phone = models.CharField(verbose_name='phone number', max_length=16)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_uploads)
