from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from services.formatting import data_formatting


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    storage_limit = models.PositiveIntegerField(_("storage limit"), default=10240)
    used_storage = models.PositiveIntegerField(_("used storage"), default=0)

    def validate_unique_username(self):
        if User.objects.filter(username=self.username).exclude(pk=self.pk).exists():
            raise ValidationError({'username': _("The username already exists.")})

    def validate_unique_email(self):
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({"email": _("The email address is already in use.")})

    def clean(self):
        super().clean()
        self.first_name = data_formatting(self.first_name, True)
        self.last_name = data_formatting(self.last_name, True)
        self.username = data_formatting(self.username, is_required_field=True)
        self.email = data_formatting(self.email, is_required_field=True)
        self.validate_unique_username()
        self.validate_unique_email()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}: {self.email} ({self.used_storage}/{self.storage_limit}mb)"
