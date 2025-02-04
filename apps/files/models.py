import os.path

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
# from apps.folders.models import Folder


def path_file(instance, filename):
    if instance.folder:
        return f"{instance.folder.get_full_path()}/{filename}"
    else:
        return f"uploads/{filename}"


class File(models.Model):
    folder = models.ForeignKey(
        'folders.Folder',
        on_delete=models.CASCADE,
        related_name='files',
        null=True, blank=True,
        verbose_name=_("folder file")
    )
    file = models.FileField(upload_to=path_file, verbose_name=_("file"))
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("owner"),
        null=True, blank=True,
        related_name="files",
    )

    @property
    def file_name(self):
        return os.path.basename(self.file.name)

    @property
    def file_extension(self):
        return os.path.splitext(self.file.name)[-1].lower()

    def delete(self, *args, **kwargs):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()

    def hard_delete(self):
        if self.file and os.path.exists(self.file.path):
            os.remove(self.file.path)
        super().delete()

    def restore(self):
        if self.is_deleted:
            self.is_deleted = False
            self.save()

    def __str__(self):
        return self.file.path

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")
