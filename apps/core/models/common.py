from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models.base import BaseModel
import datetime


class Attachment(BaseModel):
    def get_attachment_path(instance, filename):
        """Generate unique file path for attachments"""
        ext = filename.split('.')[-1]
        prefix = f"{instance.content_type.model}_attachment"
        filename = f'{prefix}_{datetime.datetime.now().timestamp()}.{ext}'
        return f'attachments/{instance.org.id}/{filename}'

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_attachment_path)  # Updated this line
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.file:
            # Update file size when file is uploaded
            self.file_size = self.file.size
            # Set file type based on extension
            self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)
