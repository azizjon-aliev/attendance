from datetime import datetime
from django.db import models


class Group(models.Model):
    """ Группа """
    sub_group = models.CharField(verbose_name='Под группа', max_length=2, null=False, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ])
    language = models.CharField(verbose_name='Язык', max_length=2, null=False, choices=[
        ('tj', 'tj'),
        ('ru', 'ru'),
        ('en', 'en'),
    ])
    course = models.CharField(verbose_name='Курс', max_length=10, null=False, choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ])

    def __str__(self):
        return f"{self.sub_group} {self.language} {self.course}"

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Student(models.Model):
    """ Студенты """
    fio = models.CharField(verbose_name='ФИО', max_length=150)
    group = models.ForeignKey(Group, verbose_name='Группа', blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Attendance(models.Model):
    """ Посещаемость """
    group = models.ForeignKey(Group, verbose_name='Группа', blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата', null=False, default=datetime.now())

    def __str__(self):
        return f"{self.group} {self.date}"

    class Meta:
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемости'



class AttendanceStatus(models.Model):
    """ """
    attendance = models.ForeignKey(Attendance, verbose_name='Посещаемость', blank=False, null=False,
                                   on_delete=models.CASCADE)
    students = models.ForeignKey(Student, verbose_name='Студент', blank=False, null=False, on_delete=models.CASCADE)
    time_1 = models.IntegerField(verbose_name="1", default=0)
    time_2 = models.IntegerField(verbose_name="2", default=0)
    time_3 = models.IntegerField(verbose_name="3", default=0)
    time_4 = models.IntegerField(verbose_name="4", default=0)
    time_5 = models.IntegerField(verbose_name="5", default=0)
