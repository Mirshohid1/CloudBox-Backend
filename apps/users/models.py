from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from config.utils import data_formatting


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    storage_limit = models.PositiveIntegerField(_("storage limit"), default=10240)
    used_storage = models.PositiveIntegerField(_("used storage"), default=0)

    @staticmethod
    def validate_unique_username(username):
        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': _("The username already exists.")})

    @staticmethod
    def validate_unique_email(email):
        if User.objects.filter(email=email).exists():
            raise ValidationError({"email": _("The email address is already in use.")})

    def clean(self):
        super().clean()
        self.first_name = data_formatting(self.first_name, is_name=True, is_required_field=False)
        self.last_name = data_formatting(self.last_name, is_name=True, is_required_field=False)
        self.username = data_formatting(self.username)
        self.email = data_formatting(self.email)
        self.validate_unique_username()
        self.validate_unique_email()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}: {self.email} ({self.used_storage}/{self.storage_limit}mb)"
