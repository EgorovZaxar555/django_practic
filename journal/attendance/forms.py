from django import forms
from .models import Student
from django.forms import ModelForm, TextInput


class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'group']
        # widgets: {
        #     "title": TextInput(attrs={
        #         'class': 'form-control'
        #     }),
        #     "first_name": TextInput(attrs={
        #         'class': 'form-control'
        #     }),
        #     "group": TextInput(attrs={
        #         'class': 'form-control'
        #     }),         
        # }
        


class StudentForm(forms.Form):
    last_name = forms.CharField(max_length=100, label="Фамилия")
    first_name = forms.CharField(max_length=100, label="Имя")
    group = forms.CharField(max_length=20, label="Группа")