from django.db import models
from django.contrib.auth.models import User


def avatar_uploads(instance: User, filename) -> str:
    return 'users/user_{pk}/avatar/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=100, unique=True)
    phone = models.CharField(verbose_name='phone number', max_length=16)
    email = models.EmailField(unique=True)
    avatar = models.OneToOneField('Avatar', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user}'


class Avatar(models.Model):
    src = models.ImageField(null=True, blank=True, upload_to=avatar_uploads)
    alt = models.CharField(max_length=100)

    def __str__(self):
        return f'url: {self.src}, alt: {self.alt}'

