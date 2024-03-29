# Generated by Django 4.1.7 on 2023-03-11 05:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_alter_attendance_date_alter_specialty_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='typeOfTraining',
            field=models.CharField(choices=[('рӯзона', 'рӯзона'), ('фосилави', 'фосилави')], default=1, max_length=30, verbose_name='Вид обучения'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 3, 11, 10, 29, 26, 212497), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.faculty', verbose_name='Факультет'),
        ),
        migrations.AlterField(
            model_name='group',
            name='language',
            field=models.CharField(choices=[('тч', 'таджикский'), ('р', 'русский'), ('ан', 'английский')], max_length=2, verbose_name='Язык'),
        ),
        migrations.AlterField(
            model_name='group',
            name='sub_group',
            field=models.CharField(choices=[('а', 'а'), ('б', 'б'), ('в', 'в'), ('г', 'г'), ('д', 'д')], max_length=2, verbose_name='Под группа'),
        ),
    ]
