from pathlib import Path
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from .models import Student
from .forms import StudentModelForm, StudentAvatarForm

# Create your views here.

def index(request):
    return render(request, 'attendance/index.html')

@login_required
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    if request.user.is_student and request.user.student_profile.id != student.id:
        return render(request, 'attendance/no_access.html', status=403)
        
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
        return redirect('student_detail', id=user.student_profile.id)
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



def upload_raw(request):
    if request.method == "POST" and request.FILES.get("file_upload"):
        f = request.FILES["file_upload"]
        dest = Path(settings.MEDIA_ROOT) / "raw" / f.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb+") as out:
            for chunk in f.chunks():
                out.write(chunk)
        return HttpResponse(f"Загружено: {dest}")
    return render(request, "attendance/upload_raw.html")     


@login_required
def student_avatar_update(request):
    u = request.user
    if not (u.is_authenticated and getattr(u, "is_student", False)):
        return render(request, "attendance/no_access.html", status=403) 

    student = u.student_profile
    if request.method == "POST":
        form = StudentAvatarForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Аватар обновлён")
            return redirect("role-redirect")          
    else:
        form = StudentAvatarForm(instance=student)
    return render(request, "attendance/avatar_form.html", {"form": form}) 