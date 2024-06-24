from django.db import models
from django.contrib.auth.hashers import make_password, check_password


from users.constants import USER_ROLE_CHOICES


# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=100, choices=USER_ROLE_CHOICES, null=False, blank=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.user_name

