from django.db import models


class UserInfo(models.Model):
    name = models.CharField(max_length=50, unique=True)
    passwd = models.CharField(max_length=128)
    phone = models.CharField(max_length=12, unique=True)
    avatar = models. URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)