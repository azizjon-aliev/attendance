from django.core.exceptions import ValidationError
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from attendance import models


class FacultyResource(resources.ModelResource):
    # published = Field(attribute='published', column_name='published_date')
    title = Field(attribute='title', column_name='Названия')

    # author = fields.Field(
    #     column_name='author',
    #     attribute='author',
    #     widget=ForeignKeyWidget(Author, field='name'))

    def before_import_row(self, row, **kwargs):
        title = row.get("Названия")
        (faculty, _created) = models.Faculty.objects.get_or_create(title=title, defaults={"title": title})
        row['Названия'] = faculty.title
        # print(type(a), a[0])

    # def before_export(queryset, *args, **kwargs)
    #     pass


    class Meta:
        model = models.Faculty
        fields = ('id', 'title',)
        # fields = ('author__name',)

class DepartmentResource(resources.ModelResource):
    title = Field(attribute='title', column_name='Названия')
    faculty = Field(
        attribute='faculty',
        column_name='Факультет',
        widget=ForeignKeyWidget(models.Faculty, field='title'),
    )
    def before_import_row(self, row, **kwargs):
        faculty__title = row.get("Факультет")
        (faculty, _created) = models.Faculty.objects.get_or_create(title=faculty__title, defaults={"title": faculty__title})
        row['Факультет'] = faculty.title

    class Meta:
        model = models.Department

class SpecialtyResource(resources.ModelResource):
    number = Field(attribute='number', column_name='Номер')
    title = Field(attribute='title', column_name='Названия')
    department = Field(
        attribute='department',
        column_name='Кафедра',
        widget=ForeignKeyWidget(models.Faculty, field='title'),
    )
    def before_import_row(self, row, **kwargs):
        department__title = row.get("Кафедра")
        (department, _created) = models.Department.objects.get_or_create(title=department__title, defaults={"title": department__title})
        row['Кафедра'] = department.title

    class Meta:
        model = models.Specialty


class GroupResource(resources.ModelResource):
    sub_group = Field(attribute='sub_group', column_name='Под группа')
    language = Field(attribute='language', column_name='Язык')
    course = Field(attribute='course', column_name='Курс')
    typeOfTraining = Field(attribute='typeOfTraining', column_name='Вид обучения')
    specialty = Field(
        attribute='specialty',
        column_name='Специальность',
        widget=ForeignKeyWidget(models.Specialty, field='title'),
    )
    def before_import_row(self, row, **kwargs):
        specialty__title = row.get("Специальность")
        (specialty, _created) = models.Specialty.objects.get_or_create(title=specialty__title, defaults={"title": specialty__title})
        row['Специальность'] = specialty.title

    class Meta:
        model = models.Group


class StudentResource(resources.ModelResource):
    fio = Field(attribute='fio', column_name='ФИО')
    group = Field(
        attribute='group',
        column_name='Группа',
        widget=ForeignKeyWidget(models.Group, field='id'),
    )
    def before_import_row(self, row, **kwargs):
        number, sub_group, course, language, typeOfTraining = [data.strip() for data in row.get('Группа').split(',')]
        course = course.replace('курси', '')

        try:
            specialty = models.Specialty.objects.get(number=number)
            (group, _) = models.Group.objects.get_or_create(
                specialty=specialty,
                sub_group=sub_group,
                course=course,
                language=language,
                typeOfTraining=typeOfTraining,
                defaults={
                    'specialty': specialty,
                    'sub_group': sub_group,
                    'course': course,
                    'language': language,
                    'typeOfTraining': typeOfTraining,
                }
            )

            row['Группа'] = group.id
        except Exception:
            raise ValidationError("Неверный формат группа")

    class Meta:
        model = models.Student
