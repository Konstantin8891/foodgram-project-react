from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    Role_choices =(
        ('User', 'authorized'),
        ('Admin', 'admin')
    ) 
    first_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=Role_choices)

    class Meta:
        unique_together = ('username', 'email')