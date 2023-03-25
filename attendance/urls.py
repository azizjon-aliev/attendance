from django.contrib import admin
from django.urls import path
from attendance import views

urlpatterns = [
    path('attendances/export/excel/', views.export_attendances_xls, name='export_excel'),
    path("students/", views.students, name="students"),
    path("attendances/", views.get_attendance, name="attendance"),
    path("attendances/add", views.create_attendance, name="attendance-create"),
    path("attendances/edit", views.update_attendance, name="attendance-update"),
]