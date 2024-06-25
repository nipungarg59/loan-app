from django.db import models


class UserManager(models.Manager):

    def __init__(self) -> None:
        super().__init__()

    def get_by_user_name(self, user_name):
        return self.filter(user_name=user_name)

    def authenticate(self, user_name, password):
        users = self.get_by_user_name(user_name)
        if users:
            user = users.first()
            if user.check_password(password):
                return user
        return None
