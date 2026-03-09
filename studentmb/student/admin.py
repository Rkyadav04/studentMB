# Register your models here.
from django.contrib import admin
from .models import Student, StudentDocument

class StudentDocumentInline(admin.TabularInline):
    model = StudentDocument
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'course', 'email', 'contact', 'status']
    inlines = [StudentDocumentInline]

admin.site.register(Student, StudentAdmin)
admin.site.register(StudentDocument)
