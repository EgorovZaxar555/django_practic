from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentModelForm

# Create your views here.

def index(request):
    return render(request, 'attendance/index.html')

def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'attendance/student_detail.html', {'student': student})


@login_required
def student_list(request):
    if not request.user.is_teacher:
        return render(request, 'attendance/no_access.html', {'title': f'y вас нет доступа'}, )
    students = Student.objects.all()
    return render(request, "attendance/student_list.html", {"students": students})


@login_required
def profile_dispatch(request):
    user = request.user
    if user.is_student:
        return render(request, 'attendance/index.html')
    elif user.is_teacher:
        return render(request, 'attendance/index.html')
    else:
        return render(request, 'attendance/index.html')





def add_student(request):
    if request.method == "POST":
        form = StudentModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentModelForm()
    return render(request, "attendance/add_student.html", {"form": form})