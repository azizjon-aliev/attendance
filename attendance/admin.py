from django.contrib import admin
from attendance import models
from attendance.models import Group, Attendance, AttendanceStatus
from import_export.admin import ImportExportMixin

from attendance.resources import FacultyResource, DepartmentResource, SpecialtyResource, GroupResource, StudentResource
from attendance.utils import custom_titled_filter


@admin.register(models.Faculty)
class FacultyAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_classes = [FacultyResource]
    search_fields = ("title", )


@admin.register(models.Department)
class DepartmentAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_classes = [DepartmentResource]
    list_display = ("title", "faculty", )
    list_filter = (("faculty__title", custom_titled_filter('Факультет')),)
    search_fields = ("title", "faculty__title", )
    autocomplete_fields = ['faculty']

@admin.register(models.Specialty)
class SpecialtyAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_classes = [SpecialtyResource]
    list_display = ("number", "title", "department", )
    list_filter = (("department__title", custom_titled_filter('Кафедра')),)
    search_fields = ("number", "title", "department__title",)
    autocomplete_fields = ['department']

@admin.register(models.Group)
class GroupAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_classes = [GroupResource]
    list_display = ("sub_group", "language", "course", "specialty", )
    list_filter = ("language", "course", ('specialty__title', custom_titled_filter('Специальность')),)
    search_fields = ("sub_group", "language", "course", "specialty__title", )
    autocomplete_fields = ['specialty']

@admin.register(models.Student)
class StudentAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = StudentResource
    list_display = ("fio", "group", )
    list_filter = (
        "group", "group__course",
        ('group__specialty__title', custom_titled_filter('Специальность')),
        ('group__typeOfTraining', custom_titled_filter('Вид обучения')),
    )
    search_fields = ("fio", )
    autocomplete_fields = ['group']


@admin.register(models.Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        attendance = Attendance.objects.get(id=object_id)
        students = AttendanceStatus.objects.filter(attendance_id=attendance.id).values(
            'students__fio',
            'students_id',
            'time_1',
            'time_2',
            'time_3',
            'time_4',
            'time_5',
        )
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
