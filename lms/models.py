from django.db import models

from config import NULLABLE


# Create your models here.


class Course(models.Model):

    title = models.CharField(max_length=128, verbose_name='название')
    preview = models.ImageField(upload_to='previews/courses/', **NULLABLE, verbose_name='превью')
    description = models.TextField(verbose_name='описание')

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return f'{self.title}'


class Lesson(models.Model):
    title = models.CharField(max_length=128, verbose_name='название')
    preview = models.ImageField(upload_to='previews/lessons/', **NULLABLE, verbose_name='превью')
    description = models.TextField(verbose_name='описание')
    url = models.CharField(max_length=256, verbose_name='ссылка')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return f'{self.title}'
