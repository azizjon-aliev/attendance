# Generated by Django 4.1.7 on 2023-02-25 02:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2023, 2, 25, 7, 55, 36, 966664), verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Посещаемость',
                'verbose_name_plural': 'Посещаемости',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_group', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=2, verbose_name='Под группа')),
                ('language', models.CharField(choices=[('tj', 'tj'), ('ru', 'ru'), ('en', 'en')], max_length=2, verbose_name='Язык')),
                ('course', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=10, verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=150, verbose_name='ФИО')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.group', verbose_name='Группа')),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
            },
        ),
        migrations.CreateModel(
            name='AttendanceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_1', models.BooleanField(default=True, verbose_name='1')),
                ('time_2', models.BooleanField(default=True, verbose_name='2')),
                ('time_3', models.BooleanField(default=True, verbose_name='3')),
                ('time_4', models.BooleanField(default=True, verbose_name='4')),
                ('time_5', models.BooleanField(default=True, verbose_name='5')),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.attendance', verbose_name='Посещаемость')),
                ('students', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.student', verbose_name='Студент')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.group', verbose_name='Группа'),
        ),
    ]
