from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='attendance_index'),
    path('student/<int:id>/', views.student_detail, name='student_detail'),
    path('students/', views.student_list, name='student_list'),
]
