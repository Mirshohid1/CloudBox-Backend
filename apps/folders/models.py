import os
import shutil

from django.db import models
from django.utils.translation import gettext_lazy as _
from ..users.models import User
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

    def delete(self, *args, **kwargs):
        folder_path = self.get_full_path()

        for subfolder in self.subfolders.all():
            subfolder.delete(*args, *kwargs)

        if os.path.exists(folder_path):
            print(folder_path)
            try:
                os.rmdir(folder_path)
            except OSError:
                shutil.rmtree(folder_path)


        super().delete(*args, **kwargs)

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
