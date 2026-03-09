from django.db import models
from django.utils import timezone

created_at = models.DateTimeField(default=timezone.now)
updated_at = models.DateTimeField(default=timezone.now)

from django.contrib.auth.models import User

class Profile(models.Model):
    USER_ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)  # store OTP temporarily
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Create your models here.
from django.db import models

STATUS_CHOICE = (
    ('active','Active'),
    ('inactive','Inactive'),
)
class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)   
    email = models.EmailField(max_length=100 , null=True , blank=True)
    last_result = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    def __str__(self):
        return f"{self.name} ({self.student_id})"
    

class StudentDocument(models.Model):
    student = models.ForeignKey(Student, related_name='documents', on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
   
    def __str__(self):
        return f"{self.student.name} - {self.file.name}"

    
