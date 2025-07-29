# Create your views here.
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student,  StudentDocument
from django.db.models import Q
from .forms import StudentForm
from django.http import HttpResponse
from django.utils.timezone import now

import csv
from django.http import HttpResponse
import csv
from django.http import HttpResponse

from django.utils.timezone import now
from datetime import datetime

def home(request):
    student_id = request.GET.get("student_id", "")
    name = request.GET.get("name", "")
    course = request.GET.get("course", "")
    contact = request.GET.get("contact", "")
    status = request.GET.get("status", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    students = Student.objects.filter(is_deleted=False)
    
    

    if student_id:
        students = students.filter(student_id__icontains=student_id)
    if name:
        students = students.filter(name__icontains=name)
    if course:
        students = students.filter(course__icontains=course)
    if contact:
        students = students.filter(contact__icontains=contact)
    if status:
        students = students.filter(status=status)
    if start_date:
        students = students.filter(created_at__date__gte=start_date)
    if end_date:
        students = students.filter(created_at__date__lte=end_date)

    # CSV Export for filtered results
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="filtered_students.csv"'
        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Name', 'Course', 'Contact', 'Email', 'Last Result', 'Status', 'Created At', 'Updated At'])
        for s in students:
            writer.writerow([
                s.student_id, s.name, s.course, s.contact, s.email,
                s.last_result, s.status,
                s.created_at.strftime("%Y-%m-%d %H:%M"),
                s.updated_at.strftime("%Y-%m-%d %H:%M")
            ])
        return response

    # Pagination
    paginator = Paginator(students.order_by('-created_at'), 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student/home.html', {
        'page_obj': page_obj,
        'filters': {
            'student_id': student_id,
            'name': name,
            'course': course,
            'contact': contact,
            'status': status,
            'start_date': start_date,
            'end_date': end_date
        },
        'created_today': students.filter(created_at__date=now().date())
    })



def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect('home')  # ensure this matches your url name
        else:
            messages.error(request, "There was an error with the form.")
    else:
        form = StudentForm()
    return render(request, 'student/add.html', {'form': form})

    
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.student_id = request.POST.get('student_id' ,'')
        student.name = request.POST.get('name' ,'')
        student.course = request.POST.get('course' ,'')
        student.contact = request.POST.get('contact', '')
        student.email = request.POST.get('email', '')
        student.last_result = request.POST.get('last_result' ,'')
        student.status = request.POST.get('status' ,'')
        student.save()
        return redirect('home')
    return render(request, 'student/edit.html', {'student': student})


def upload_document(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        for f in request.FILES.getlist('file'):
            StudentDocument.objects.create(student=student, file=f)
        messages.success(request, "Document(s) uploaded successfully.")

    document = student.documents.all()  # load updated documents
    return render(request, 'student/upload_documents.html', {
        'student': student,
        'documents': document
    })



def soft_delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.is_deleted = True
    student.save()
    return redirect('home')

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('home')

def toggle_status(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.status = 'inactive' if student.status == 'active' else 'active'
    student.save()
    return redirect('home')  


def student_list(request):
    query = request.GET.get('q')
    course = request.GET.get('course')
    status = request.GET.get('status')

    students = Student.objects.filter(is_deleted=False)

    # Search filter (name, ID, contact, email)
    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(contact__icontains=query) |
            Q(email__icontains=query)
        )

    # Course filter
    if course:
        students = students.filter(course=course)

    # Status filter
    if status:
        students = students.filter(status=status)

    # Paginate the result (25 per page)
    paginator = Paginator(students.order_by('-created_at'), 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass filters back to template for persistence
    context = {
        'page_obj': page_obj,
        'query': query,
        'course_filter': course,
        'status_filter': status,
        'courses_list': Student.objects.values_list('course', flat=True).distinct()[:10],
        'statuses_list': Student.objects.values_list('status', flat=True).distinct()[:5],
    }
    return render(request, 'student/student_list.html', context)

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    documents = student.documents.all()
    return render(request, 'student/student_detail.html', {'student': student, 'documents': documents})


def created_at_view(request):
    query = request.GET.get("q", "")
    students = Student.objects.filter(is_deleted=False).order_by('-created_at')

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(course__icontains=query) |
            Q(email__icontains=query) |
            Q(contact__icontains=query)
        )

    # Handle CSV export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="created_at_students.csv"'
        writer = csv.writer(response)

        # Header
        writer.writerow(['Student ID', 'Name', 'Course', 'Contact', 'Email', 'Last Result', 'Status', 'Created At', 'Updated At'])

        # Rows
        for s in students:
            writer.writerow([
                s.student_id, s.name, s.course, s.contact, s.email,
                s.last_result, s.status,
                s.created_at.strftime("%Y-%m-%d %H:%M"),
                s.updated_at.strftime("%Y-%m-%d %H:%M")
            ])
        return response

    return render(request, 'student/created_at_list.html', {
        'students': students,
        'query': query
    })

def export_csv(request):
    students = Student.objects.all()

    student_id = request.GET.get("student_id", "").strip()
    name = request.GET.get("name", "").strip()
    course = request.GET.get("course", "").strip()
    contact = request.GET.get("contact", "").strip()
    status = request.GET.get("status", "")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if student_id:
        students = students.filter(student_id__icontains=student_id)
    if name:
        students = students.filter(name__icontains=name)
    if course:
        students = students.filter(course__icontains=course)
    if contact:
        students = students.filter(contact__icontains=contact)
    if status:
        students = students.filter(status=status)
    if start_date and end_date:
        students = students.filter(created_at__date__range=[start_date, end_date])

    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=students.csv'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Course', 'Contact', 'Status', 'Created At'])

    for student in students:
        writer.writerow([
            student.student_id,
            student.name,
            student.course,
            student.contact,
            student.status,
            student.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


#student login page
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'student/login.html', {'error': 'Invalid credentials'})
    return render(request, 'student/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



