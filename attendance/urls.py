from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from attendance import views
from core import settings

urlpatterns = [
    path("students/", views.students, name="students"),
    path("attendances/", views.get_attendance, name="attendance"),
    path("attendances/add", views.create_attendance, name="attendance-create"),
    path("attendances/edit", views.update_attendance, name="attendance-update"),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]