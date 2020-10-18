from django.db import models
from django.utils import timezone
import uuid


class Banger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nkdsu_id = models.CharField(max_length=255)
    title = models.TextField(blank=True)
    artist = models.TextField(blank=True)
    role = models.TextField(blank=True)
    certificate = models.FileField()
    certified_timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.artist})"
