from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, null=True, unique=True)
    full_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
