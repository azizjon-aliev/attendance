from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from attendance import views
from core import settings

urlpatterns = [
    path("students/", views.students, name="students"),
    path("attendance/", views.attendances, name="attendance"),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]