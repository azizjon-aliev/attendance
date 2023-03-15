# Generated by Django 4.1.7 on 2023-03-11 07:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_group_typeoftraining_alter_attendance_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 3, 11, 12, 29, 9, 466653), verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='group',
            name='language',
            field=models.CharField(choices=[('таджикский', 'таджикский'), ('русский', 'русский'), ('английский', 'английский')], max_length=15, verbose_name='Язык'),
        ),
    ]
