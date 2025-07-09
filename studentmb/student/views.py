# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student

def home(request):
    student = Student.objects.all()
    return render(request, 'student/home.html', {'student': student })

def add_student(request):
    if request.method == 'POST':
        Student.objects.create(
            student_id=request.POST['student_id'],
            name=request.POST['name'],
            course=request.POST['course'],
            contact=request.POST['contact'],
            last_result=request.POST['last_result'],
        )
        return redirect('home')
    return render(request, 'student/add.html')

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.student_id = request.POST.get('student_id' ,'')
        student.name = request.POST.get('name' ,'')
        student.course = request.POST.get('course' ,'')
        student.contact = request.POST.get('contact', '')
        student.last_result = request.POST.get('last_result' ,'')
        student.save()
        return redirect('home')
    return render(request, 'student/edit.html', {'student': student})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('home')

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


