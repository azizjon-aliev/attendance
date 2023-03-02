from django.db.models import Sum
from django.shortcuts import render
from .models import Attendance, AttendanceStatus, Group, Student
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse, HttpResponseBadRequest


def students(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'GET':
            group_id = request.GET.get('group')
            data = Student.objects.filter(group_id=group_id).values()
            return JsonResponse({'data': list(data)})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def attendances(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'GET':
            date_start = request.GET.get('date-start')
            date_end = request.GET.get('date-end')
            group_id = request.GET.get('group')

            if date_end:
                attendance = AttendanceStatus.objects.filter(attendance__date__range=[date_start, date_end],
                                                             attendance__group_id=group_id)
            else:
                attendance = AttendanceStatus.objects.filter(attendance__date=date_start,
                                                             attendance__group_id=group_id)

            data = attendance.values('students__fio').annotate(
                time_1=Sum('time_1'),
                time_2=Sum('time_2'),
                time_3=Sum('time_3'),
                time_4=Sum('time_4'),
                time_5=Sum('time_5'),
            ).order_by('students_id')

            return JsonResponse({
                'data': list(data)
            })

        if request.method == "POST":
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



        if request.method == "PUT":
            pk = request.PUT.get("attendance_id")
            date = request.PUT.get("date")
            students = request.POST.get("students")
            total = int(request.PUT.get('total_students'))

            # if Attendance.objects.filter(group_id=group, date=date):
            #     return JsonResponse({"errors": "Вы не можете добавить данные в эту группу и день"}, status=422)
            #
            # attendance = Attendance(group_id=group, date=date)
            # attendance.save()
            #
            # for i in range(total_students):
            #     s_id = request.POST.get(f"students[{i}][id]")
            #     s_time_1 = 1 if request.POST.get(f"students[{i}][time_1]", 0) == "true" else 0
            #     s_time_2 = 1 if request.POST.get(f"students[{i}][time_2]", 0) == "true" else 0
            #     s_time_3 = 1 if request.POST.get(f"students[{i}][time_3]", 0) == "true" else 0
            #     s_time_4 = 1 if request.POST.get(f"students[{i}][time_4]", 0) == "true" else 0
            #     s_time_5 = 1 if request.POST.get(f"students[{i}][time_5]", 0) == "true" else 0
            #
            #     attendanceStatus = AttendanceStatus(attendance=attendance, students_id=s_id, time_1=s_time_1,
            #                                         time_2=s_time_2,
            #                                         time_3=s_time_3, time_4=s_time_4, time_5=s_time_5)
            #     attendanceStatus.save()

            return JsonResponse({"message": "Success"})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
