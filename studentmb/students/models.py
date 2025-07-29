from django.db import models

# Create your models here.
class Meta:
    indexes = [
        models.Index(fields=['student_id']),
        models.Index(fields=['course']),
        models.Index(fields=['status']),
        models.Index(fields=['email']),
    ]
