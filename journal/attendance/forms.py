from django import forms
from django.core.validators import FileExtensionValidator
from .models import Student

MAX_MB = 5

def validate_filesize(file):
    if file.size > MAX_MB * 1024 * 1024:
        raise forms.ValidationError(f"Размер файла не должен превышать {MAX_MB} МБ")


class StudentAvatarForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["avatar"]
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"accept": "image/*"})
        }
        help_texts = {"avatar": "Загрузите изображение (JPEG/PNG), до 5 МБ"}

    avatar = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_filesize
        ],
        label="Аватар"
    )

class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'group']


class StudentForm(forms.Form):
    last_name = forms.CharField(max_length=100, label="Фамилия")
    first_name = forms.CharField(max_length=100, label="Имя")
    group = forms.CharField(max_length=20, label="Группа")