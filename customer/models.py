from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(verbose_name='Date of birth')

    def __str__(self):
        return self.user.first_name

    @property
    def name(self):
        return f'{self.user.first_name} {self.user.last_name}'
