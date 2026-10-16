from django.shortcuts import render, get_object_or_404
from .models import Student

# Create your views here.

def index(request):
    return render(request, 'attendance/index.html')

def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'attendance/student_detail.html', {'student': student})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/student_list.html', {'students': students})
