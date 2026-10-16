from django.db import models

# Create your models here.

class Student(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    group = models.CharField(max_length=20, verbose_name="Группа")

    def __str__(self):
        return f"{self.last_name} {self.first_name[0]} {self.patronymic[0]}"


class Teacher(models. Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")

    def __str__(self):
        return f"{self.last_name} {self.first_name[0]} {self.patronymic[0]}"


class Lesson(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.CharField(max_length=50, verbose_name="Аудитория")

    def __str__(self):
        return f"{self.subject} ({self.date})"


class Attendance(models. Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.student} {self.lesson}: {'✔' if self.present else 'X'}"