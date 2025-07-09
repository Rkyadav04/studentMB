from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    last_result = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.student_id})"
