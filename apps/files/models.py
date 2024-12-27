import os.path

from django.db import models
from django.utils.translation import gettext_lazy as _
from ..users.models import User
from ..folders.models import Folder


def path_file(instance, filename):
    if instance.folder:
        return f"{instance.folder.get_full_path()}/{filename}"
    else:
        return f"uploads/{filename}"


class File(models.Model):
    folder = models.ForeignKey(
        Folder,
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
    )

    @property
    def file_name(self):
        return os.path.basename(self.file.name)

    @property
    def file_extension(self):
        return os.path.splitext(self.file.name)[-1].lower()

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.exists(self.file.path):
                os.remove(self.file.path)
                print(f"File {self.file.path} deleted.")

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.file.path
