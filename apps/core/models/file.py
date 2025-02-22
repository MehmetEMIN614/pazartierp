import hashlib

import magic
from PIL import Image
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.utils.file_management import generate_r2_upload_path, validate_file


class FileRecord(models.Model):
    """
    Unified model for file and image management
    Supports both generic files and images with flexible metadata
    """

    class FileType(models.TextChoices):
        """Enumeration of file types"""
        FILE = 'FILE', _('Generic File')
        IMAGE = 'IMAGE', _('Image')
        DOCUMENT = 'DOCUMENT', _('Document')
        ARCHIVE = 'ARCHIVE', _('Archive')

    # Basic metadata
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    # File field with flexible upload and validation
    file = models.FileField(
        upload_to=generate_r2_upload_path,
        validators=[validate_file]
    )

    # Generic foreign key for flexible file attachment
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Enhanced metadata
    file_type = models.CharField(
        max_length=10,
        choices=FileType.choices,
        default=FileType.FILE
    )
    mime_type = models.CharField(max_length=100)
    file_size = models.IntegerField()
    file_hash = models.CharField(max_length=64)  # SHA-256 hash
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Image-specific fields (optional)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    alt_text = models.CharField(max_length=255, null=True, blank=True)

    # Additional tracking
    is_public = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    last_downloaded = models.DateTimeField(null=True)
    is_primary = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Override save to:
        1. Generate file hash
        2. Set metadata
        3. Extract image dimensions if applicable
        """
        if self.file:
            # Generate file hash
            sha256 = hashlib.sha256()
            for chunk in self.file.chunks():
                sha256.update(chunk)
            self.file_hash = sha256.hexdigest()

            # Set metadata
            self.file_size = self.file.size
            self.mime_type = magic.from_buffer(self.file.read(1024), mime=True)
            self.file.seek(0)

            # Determine file type based on mime type
            mime_to_type = {
                'image/jpeg': self.FileType.IMAGE,
                'image/png': self.FileType.IMAGE,
                'image/gif': self.FileType.IMAGE,
                'image/webp': self.FileType.IMAGE,
                'application/pdf': self.FileType.DOCUMENT,
                'application/msword': self.FileType.DOCUMENT,
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': self.FileType.DOCUMENT,
                'application/zip': self.FileType.ARCHIVE,
                'application/x-rar-compressed': self.FileType.ARCHIVE,
            }
            self.file_type = mime_to_type.get(self.mime_type, self.FileType.FILE)

            # Extract image dimensions if it's an image
            if self.file_type == self.FileType.IMAGE:
                try:
                    with Image.open(self.file) as img:
                        self.width, self.height = img.size
                except Exception:
                    # Fallback if image dimensions can't be extracted
                    self.width = self.height = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")
        ordering = ['-uploaded_at']
