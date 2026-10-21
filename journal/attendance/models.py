from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid
from datetime import datetime
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


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


def avatar_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    uid = uuid.uuid4().hex
    today = datetime.now().strftime("%Y/%m/%d")
    return f"avatars/{today}/{uid}{ext}"



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
    avatar = models.ImageField(upload_to=avatar_upload_to, default='avatars/default.jpg')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

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

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Lesson(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.CharField(max_length=50, verbose_name="Аудитория")

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return f"{self.subject} ({self.date})"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемость'

    def __str__(self):
        return f"{self.student} {self.lesson}: {'✔' if self.present else 'X'}"




def _delete_file(path):
    try:
        if path and os.path.isfile(path):
            os.remove(path)
    except Exception:
        pass


@receiver(post_delete, sender=Student)
def _student_avatar_delete_file(sender, instance, **kwargs):
    if instance.avatar and instance.avatar.name != "avatars/default.jpg":
        _delete_file(instance.avatar.path)


@receiver(pre_save, sender=Student)
def _student_avatar_replace_file(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Student.objects.get(pk=instance.pk)
    except Student.DoesNotExist:
        return
    new_file = instance.avatar
    if old.avatar and old.avatar != new_file and old.avatar.name != "avatars/default.jpg":
        _delete_file(old.avatar.path)