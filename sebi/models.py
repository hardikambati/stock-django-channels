from django.db import models
import uuid

# Create your models here.

class Share(models.Model):

    name = models.CharField(max_length=255, blank=False, unique=True)
    unique_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False
    )

    def __str__(self):
        return self.name