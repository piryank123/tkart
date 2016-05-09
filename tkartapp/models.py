from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Shirt(models.Model):
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    size = models.CharField(max_length=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

