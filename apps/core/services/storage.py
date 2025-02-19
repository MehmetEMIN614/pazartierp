from apps.core.models.storage import File, FileCategory, ImageAsset
from django.core.files.uploadedfile import UploadedFile
from django.contrib.contenttypes.models import ContentType
from typing import Optional


class FileService:
    @staticmethod
    def upload_file(uploaded_file: UploadedFile, org_id: int,
                    category: FileCategory, content_type: ContentType,
                    object_id: str, created_by: Optional[int] = None) -> File:
        file = File(
            name=uploaded_file.name,
            category=category,
            content_type=content_type,
            object_id=object_id,
            org_id=org_id,
            created_by_id=created_by,
            file=uploaded_file
        )
        file.save()
        return file

    @staticmethod
    def upload_image(uploaded_file: UploadedFile, org_id: int,
                     content_type: ContentType, object_id: str,
                     alt_text: str = None, is_primary: bool = False,
                     created_by: Optional[int] = None) -> ImageAsset:
        image = ImageAsset(
            name=uploaded_file.name,
            image=uploaded_file,
            content_type=content_type,
            object_id=object_id,
            org_id=org_id,
            alt_text=alt_text,
            is_primary=is_primary,
            created_by_id=created_by
        )
        image.save()
        return image