import datetime
import hashlib
import os
import secrets
from io import BytesIO

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from PIL import Image
import magic  # python-magic for file type detection

from apps.core.models.base import BaseModel


def validate_file_size(file_obj):
    """Validate file size (default: 50MB)"""
    max_size = 52428800  # 50MB in bytes
    if file_obj.size > max_size:
        raise ValidationError(_('File size must be no more than 50MB.'))


def validate_file_type(file_obj):
    """Validate file mime type"""
    allowed_types = {
        # Images
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        # Documents
        'application/pdf': '.pdf',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/vnd.ms-excel': '.xls',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        # Others can be added as needed
    }

    file_type = magic.from_buffer(file_obj.read(1024), mime=True)
    file_obj.seek(0)  # Reset file pointer after reading
    if file_type not in allowed_types:
        raise ValidationError(_('Unsupported file type.'))


def get_upload_path(instance, filename, category):
    """
    Generate file path based on category and organization
    Example: uploads/org_1/invoices/2024/03/invoice_123.pdf
    """
    ext = os.path.splitext(filename)[1].lower()
    timestamp = datetime.datetime.now()
    year = timestamp.strftime('%Y')
    month = timestamp.strftime('%m')

    filename = f"{category}_{timestamp.timestamp()}{ext}"
    return os.path.join(
        'uploads',
        f'org_{instance.org.id}',
        category,
        year,
        month,
        filename
    )


class FileCategory(BaseModel):
    """Categories for file organization"""
    name = models.CharField(max_length=100)
    allowed_types = models.JSONField(
        default=list,
        help_text=_("List of allowed file extensions")
    )
    max_file_size = models.IntegerField(
        default=52428800,  # 50MB
        help_text=_("Maximum file size in bytes")
    )

    class Meta:
        verbose_name = _("File Category")
        verbose_name_plural = _("File Categories")

    def __str__(self):
        return self.name


class File(BaseModel):
    """Central model for file management"""
    name = models.CharField(max_length=255)
    note = models.TextField(null=True, blank=True)
    category = models.ForeignKey(FileCategory, on_delete=models.PROTECT)
    file = models.FileField(
        upload_to='temp/',  # Temporary path, will be changed in save()
        validators=[validate_file_size, validate_file_type]
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    mime_type = models.CharField(max_length=100)
    file_size = models.IntegerField()
    file_hash = models.CharField(max_length=64)  # SHA-256 hash
    version = models.IntegerField(default=1)
    is_public = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    last_downloaded = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file:
            # Generate file hash
            sha256 = hashlib.sha256()
            for chunk in self.file.chunks():
                sha256.update(chunk)
            self.file_hash = sha256.hexdigest()

            # Set file size
            self.file_size = self.file.size

            # Detect mime type
            self.mime_type = magic.from_buffer(self.file.read(1024), mime=True)
            self.file.seek(0)  # Reset file pointer

            # Move file to proper location
            category_name = self.category.name.lower()
            self.file.name = get_upload_path(self, self.file.name, category_name)

        super().save(*args, **kwargs)


class ImageAsset(BaseModel):
    """Specialized model for image handling"""

    def image_upload_path(self, filename):
        return get_upload_path(self, filename, 'images')

    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to=image_upload_path  # Use named function instead of lambda
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Image Asset")
        verbose_name_plural = _("Image Assets")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            # Set image dimensions
            img = Image.open(self.image)
            self.width, self.height = img.size

        super().save(*args, **kwargs)


class TemporaryUpload(BaseModel):
    """Handle temporary file uploads before processing"""
    file = models.FileField(
        upload_to='temp_uploads/',
        validators=[validate_file_size, validate_file_type]
    )
    upload_time = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    upload_token = models.CharField(max_length=100, unique=True, editable=False)
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField(editable=False)
    mime_type = models.CharField(max_length=100, editable=False)
    chunk_size = models.IntegerField(default=0, help_text=_("Size of each chunk in bytes"))
    total_chunks = models.IntegerField(default=1)
    uploaded_chunks = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Temporary Upload")
        verbose_name_plural = _("Temporary Uploads")
        indexes = [
            models.Index(fields=['upload_token']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"{self.file_name} ({self.upload_token})"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = now() + datetime.timedelta(hours=24)
        if not self.upload_token:
            self.upload_token = secrets.token_urlsafe(32)
        if self.file:
            self.file_size = self.file.size
            self.mime_type = magic.from_buffer(self.file.read(1024), mime=True)
            self.file.seek(0)
        super().save(*args, **kwargs)

    def is_expired(self):
        """Check if the upload has expired"""
        return now() > self.expires_at

    def is_complete(self):
        """Check if all chunks have been uploaded"""
        return self.uploaded_chunks == self.total_chunks

    def cleanup(self):
        """Remove the temporary file and delete the record"""
        if self.file:
            self.file.delete(save=False)
        self.delete()

    @classmethod
    def cleanup_expired(cls):
        """Remove all expired temporary uploads"""
        expired = cls.objects.filter(expires_at__lt=now())
        for upload in expired:
            upload.cleanup()
