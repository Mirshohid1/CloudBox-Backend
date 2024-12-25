from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError


def data_formating(value: str, is_name=False) -> str:
    if value and value.strip():
        value = value.strip().capitalize() if is_name else value.strip()

    return value


class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    storage_limit = models.PositiveIntegerField(
        _("storage limit"),
        default=10240,
    )
    used_storage = models.PositiveIntegerField(
        _("used storage"),
        default=0,
        validators=[MaxValueValidator(10241)],
    )

    def clean(self):
        super().clean()

        self.first_name = data_formating(self.first_name, True)
        self.last_name = data_formating(self.last_name, True)
        self.username = data_formating(self.username)
        self.email = data_formating(self.email)

    def save(self, *args, **kwargs):
        self.clean()

        if User.objects.filter(username=self.username).exclude(pk=self.pk).exists():
            raise ValidationError({'username': "The username already exists."})
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': "The email address is already in use."})
        if ' ' in self.first_name:
            raise ValidationError({'first_name': "Spaces are not allowed in the first name."})
        if ' ' in self.last_name:
            raise ValidationError({'last_name': "Spaces are not allowed in the last name."})

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}: {self.email} ({self.used_storage}/{self.storage_limit})"
