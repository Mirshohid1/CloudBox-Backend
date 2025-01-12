import os
import shutil

from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.users.models import User
from apps.files.models import File
from config.utils import data_formatting


def get_default_parent_folder():
    folder, created = 'Folder'.objects.get_or_create(name='uploads', parent=None)
    return folder


class Folder(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        verbose_name=_("parent folder"),
        on_delete=models.CASCADE,
        null=True, blank=True,
        default=get_default_parent_folder,
        related_name='subfolders',
    )
    created_at = models.DateTimeField(_("created datetime"), auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("owner"),
        null=True, blank=True,
        related_name="folders"
    )
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()

            Folder.objects.filter(parent__id=self.id).update(is_deleted=True)
            Folder.objects.filter(folder__id=self.id).update(is_deleted=True)

    def hard_delete(self):
        subfolders = Folder.objects.filter(parent__id=self.id)
        for folder in subfolders:
            folder.hard_delete()

        files = File.objects.filter(folder__id=self.id)
        for file in files:
            file.hard_delete()

        super().delete()

    def restore(self):
        if self.is_deleted:
            self.is_deleted = False
            self.save()

            Folder.objects.filter(parent__id=self.id).update(is_deleted=False)
            File.objects.filter(folder__id=self.id).update(is_deleted=False)


    def save(self, *args, **kwargs):
        self.name = data_formatting(self.name, is_name=False)
        super().save(*args, **kwargs)

    def get_full_path(self):
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return f"uploads/{self.name}"

    def __str__(self):
        return self.get_full_path()

    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")
