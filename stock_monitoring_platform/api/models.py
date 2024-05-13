# api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import Permission

class CustomUser(AbstractUser):
    pass

class Watchlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username}'s Watchlist: {self.symbol}"

# Group._meta.get_field('user_set').related_name = 'auth_group_users'
# Permission._meta.get_field('user_set').related_name = 'auth_permission_user_set'