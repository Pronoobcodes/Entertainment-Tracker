from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, null=True, unique=True)
    full_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    groups = models.ManyToManyField('auth.Group',verbose_name='groups',blank=True,help_text='The groups this user belongs to.',related_name="customuser_groups",  related_query_name="customuser",)
    user_permissions = models.ManyToManyField('auth.Permission', verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_name="customuser_permissions",  related_query_name="customuser",)
