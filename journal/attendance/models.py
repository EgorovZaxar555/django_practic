from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):

    @property
    def is_student(self) -> bool:
        return hasattr(self, 'student_profile')

    @property
    def is_teacher(self) -> bool:
        return hasattr(self, 'teacher_profile')

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='student_profile',
        null=True, blank=True
    )
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    group = models.CharField(max_length=20, verbose_name="Группа")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='teacher_profile',
        null=True, blank=True
    )
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Lesson(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.CharField(max_length=50, verbose_name="Аудитория")

    def __str__(self):
        return f"{self.subject} ({self.date})"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.student} {self.lesson}: {'✔' if self.present else 'X'}"