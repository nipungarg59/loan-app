from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from generics.models.base_model import BaseModel
from users.constants import USER_ROLE_CHOICES
from users.managers import UserManager


# Create your models here.

class User(BaseModel):
    user_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=100, choices=USER_ROLE_CHOICES, null=False, blank=False)

    objects = UserManager()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.user_name

