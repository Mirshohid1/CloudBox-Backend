from django.db import models
from django.utils.translation import gettext_lazy as _
from ..users.models import User, data_formating


def get_default_parent_folder():
    folder, created = 'Folder'.objects.get_or_create(name='uploads', parent=None)
    return folder


class Folder(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        _("parent folder"),
        'self',
        null=True, blank=True,
        default=get_default_parent_folder,
        on_delete=models.CASCADE,
        related_name='subfolders',
    )
    created_at = models.DateTimeField(_("created datetime"), auto_now_add=True)
    owner = models.ForeignKey(
        _("owner"),
        User,
        on_delete=models.CASCADE,
    )

    def delete(self, *args, **kwargs):
        for file in self.files.all():
            file.delete()

        for subfolder in self.subfolders.all():
            subfolder.delete(*args, *kwargs)

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.name = data_formating(self.name, False)
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