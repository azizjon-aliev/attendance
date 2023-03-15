import json
import xlwt
from django.http import HttpResponse
from django.db.models import Sum, F
from django.shortcuts import render
from .models import Attendance, AttendanceStatus, Group, Student
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse, HttpResponseBadRequest


def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def get_attendance(request):
    if is_ajax(request):
        if request.method == 'GET':
            date_start = request.GET.get('date-start')
            date_end = request.GET.get('date-end')
            group_id = request.GET.get('group')
            attendance_pk = None

            if date_end:
                attendance_status = AttendanceStatus.objects.filter(attendance__date__range=[date_start, date_end],
                                                                    attendance__group_id=group_id)
            else:
                attendance = Attendance.objects.filter(date=date_start, group_id=group_id)

                if len(attendance) > 0:
                    attendance_pk = attendance[0].id

                attendance_status = AttendanceStatus.objects.filter(attendance_id=attendance_pk)

            data = attendance_status.values('students__fio').annotate(
                time_1=Sum('time_1'),
                time_2=Sum('time_2'),
                time_3=Sum('time_3'),
                time_4=Sum('time_4'),
                time_5=Sum('time_5'),
                time_total=F('time_1') + F('time_2') + F('time_3') + F('time_4') + F('time_5'),
            ).order_by('students_id')

            return JsonResponse({
                'data': list(data),
                'attendance_pk': attendance_pk,
            })
        else:
            return JsonResponse({"status": 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def create_attendance(request):
    if is_ajax(request):
        if request.method == 'POST':
            date = request.POST.get("date")
            group = request.POST.get("group")
            total_students = int(request.POST.get('total_students'))

            if Attendance.objects.filter(group_id=group, date=date):
                return JsonResponse({"errors": "Вы не можете добавить данные в эту группу и день"}, status=422)

            attendance = Attendance(group_id=group, date=date)
            attendance.save()

            for i in range(total_students):
                s_id = request.POST.get(f"students[{i}][id]")
                s_time_1 = 1 if request.POST.get(f"students[{i}][time_1]", 0) == "true" else 0
                s_time_2 = 1 if request.POST.get(f"students[{i}][time_2]", 0) == "true" else 0
                s_time_3 = 1 if request.POST.get(f"students[{i}][time_3]", 0) == "true" else 0
                s_time_4 = 1 if request.POST.get(f"students[{i}][time_4]", 0) == "true" else 0
                s_time_5 = 1 if request.POST.get(f"students[{i}][time_5]", 0) == "true" else 0

                attendanceStatus = AttendanceStatus(attendance=attendance, students_id=s_id, time_1=s_time_1,
                                                    time_2=s_time_2,
                                                    time_3=s_time_3, time_4=s_time_4, time_5=s_time_5)
                attendanceStatus.save()

            return JsonResponse({"message": "Success"})
        else:
            return JsonResponse({"status": 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def update_attendance(request):
    if is_ajax(request):
        if request.method == 'PUT':
            data = json.load(request)

            for student in data['students']:
                attendance_status = AttendanceStatus.objects.filter(attendance_id=data['attendance_id'], students_id=student['id'])
                attendance_status.update(
                    time_1=student['time_1'],
                    time_2=student['time_2'],
                    time_3=student['time_3'],
                    time_4=student['time_4'],
                    time_5=student['time_5'],
                )
            return JsonResponse({"message": 'Success update'})
        else:
            return JsonResponse({"status": 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')



def export_attendances_xls(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="attendances.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Attendances Data')  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Студент', '1 час', '2 час', '3 час', '4 час', '5 час', 'Итог']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        group_id = request.GET.get('group')
        attendance_pk = None

        print(date_start, date_end, group_id)

        if date_end:
            attendance_status = AttendanceStatus.objects.filter(attendance__date__range=[date_start, date_end],
                                                                attendance__group_id=group_id)
        else:
            attendance = Attendance.objects.filter(date=date_start, group_id=group_id)

            if len(attendance) > 0:
                attendance_pk = attendance[0].id

            attendance_status = AttendanceStatus.objects.filter(attendance_id=attendance_pk)

        rows = attendance_status.values_list('students__fio').annotate(
            time_1=Sum('time_1'),
            time_2=Sum('time_2'),
            time_3=Sum('time_3'),
            time_4=Sum('time_4'),
            time_5=Sum('time_5'),
            time_total=F('time_1') + F('time_2') + F('time_3') + F('time_4') + F('time_5'),
        ).order_by('students_id')

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)

        return response
    else:
        return HttpResponseBadRequest('Invalid request')

def students(request):
    if is_ajax(request):
        if request.method == 'GET':
            group_id = request.GET.get('group')
            data = Student.objects.filter(group_id=group_id).values()
            return JsonResponse({'data': list(data)})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


