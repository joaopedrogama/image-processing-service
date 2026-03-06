import uuid
from django.db import models
from videos.storage import get_public_storage


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', storage=get_public_storage())
    zip_video_file = models.FileField(upload_to='videos-processed/', storage=get_public_storage())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Videos'
