from django.contrib import admin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template.response import TemplateResponse
from django.urls import path
from django.views.generic import CreateView

from attendance import models
from attendance.models import Group, Attendance, AttendanceStatus


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Student)
class GroupAdmin(admin.ModelAdmin):
    pass


class AttendanceDetailView(PermissionRequiredMixin, CreateView):
    permission_required = "products.view_order"
    template_name = "admin/attendance/attendance/edit_form.html"
    model = Attendance
    fields = "__all__"


@admin.register(models.Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        attendance = Attendance.objects.get(id=object_id)
        students = AttendanceStatus.objects.filter(attendance_id=attendance.id).values('students__fio', 'students_id')
        extra_context["attendance"] = attendance
        extra_context["students"] = students
        return super(AttendanceAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['groups'] = Group.objects.all()
        return super(AttendanceAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = "Посещаемость"
        extra_context['groups'] = Group.objects.all()
        return super(AttendanceAdmin, self).changelist_view(request, extra_context=extra_context)
