import os
import uuid
from typing import Dict, List

import magic
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile


class FileUploadConfig:
    """
    Centralized configuration for file uploads
    """
    # Max file size (50MB)
    MAX_FILE_SIZE = 52_428_800

    ALLOWED_MIME_TYPES: Dict[str, List[str]] = {
        # Images
        'image/jpeg': ['.jpg', '.jpeg'],
        'image/png': ['.png'],
        'image/gif': ['.gif'],
        'image/webp': ['.webp'],

        # Documents
        'application/pdf': ['.pdf'],
        'application/msword': ['.doc'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
        'application/vnd.ms-excel': ['.xls'],
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],

        # Archives
        'application/zip': ['.zip'],
        'application/x-rar-compressed': ['.rar'],

        # Others
        'text/plain': ['.txt'],
        'text/csv': ['.csv'],
    }

    @classmethod
    def generate_unique_filename(cls, original_filename: str, prefix: str = 'file') -> str:
        """
        Generate a unique filename for storage

        :param original_filename: Original filename
        :param prefix: Optional prefix for the filename
        :return: Unique filename with preserved extension
        """
        # Extract file extension
        ext = original_filename.split('.')[-1] if '.' in original_filename else ''

        # Generate unique identifier
        unique_id = uuid.uuid4().hex[:12]

        # Construct new filename
        new_filename = f"{prefix}_{unique_id}.{ext}" if ext else f"{prefix}_{unique_id}"

        return new_filename.lower()


def validate_file(
        file_obj: UploadedFile
) -> None:
    """
    Validate file based on global settings

    :param file_obj: File to validate
    """
    # Global size check
    max_size = FileUploadConfig.MAX_FILE_SIZE

    # Check file size
    if file_obj.size > max_size:
        raise ValidationError(f'File is too large. Max size is {max_size / (1024 * 1024)}MB.')

    # Detect file type with extended safety
    try:
        file_type = magic.from_buffer(file_obj.read(1024), mime=True)
        file_obj.seek(0)  # Reset file pointer
    except Exception as e:
        raise ValidationError(f'Error detecting file type: {str(e)}')

    # Check if mime type is allowed globally
    if file_type not in FileUploadConfig.ALLOWED_MIME_TYPES:
        raise ValidationError('Unsupported file type.')


def generate_r2_upload_path(
        instance,
        filename: str
) -> str:
    """
    Generate R2-optimized upload path

    :param instance: Model instance
    :param filename: Original filename
    :return: Structured upload path
    """
    # Generate unique filename
    unique_filename = FileUploadConfig.generate_unique_filename(filename)

    # Construct path with additional context
    org_id = getattr(instance, 'org_id', 'global')

    # R2-friendly path structure
    upload_path = os.path.join(
        'uploads',
        str(org_id),
        unique_filename
    )

    return upload_path
