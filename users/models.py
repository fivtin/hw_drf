from django.contrib.auth.models import AbstractUser
from django.db import models

from config import NULLABLE
from lms.models import Course, Lesson


# Create your models here.


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, default="", **NULLABLE, verbose_name="Фамилия")

    phone = models.CharField(max_length=20, **NULLABLE, verbose_name='телефон')
    city = models.CharField(max_length=128, **NULLABLE, verbose_name='город')
    image = models.ImageField(upload_to='users/avatars/', **NULLABLE, verbose_name="аватар")

    token = models.CharField(max_length=128, verbose_name='токен', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

        # permissions = [
        #     ('view_list', 'Can view user list'),
        #     ('change_active', 'Can enable/disable active'),
        # ]

    def __str__(self):
        return f'{self.email}'


class Payment(models.Model):
    PAY_METHOD_CHOICES = {
        (1, "cash"),
        (2, "account"),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    paid_at = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='урок')
    amount = models.PositiveSmallIntegerField(verbose_name='сумма оплаты')
    method = models.PositiveSmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name='способ оплаты')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        return f'{self.user.email} - {self.paid_at}: {self.amount}[{self.method}]'
