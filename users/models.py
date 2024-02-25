from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from config import settings
from materials.models import Course, Lesson
from services import NULLABLE


class UserRoles(models.TextChoices):
    MEMBER = 'member'
    MODERATOR = 'moderator'


class User(AbstractUser):
    role = models.CharField(max_length=15, verbose_name='роль', choices=UserRoles.choices, default=UserRoles.MEMBER)

    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    city = models.CharField(max_length=150, verbose_name='Город', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Безналичная оплата'),
    ]
    payment_date = models.DateTimeField(verbose_name='Дата платежа', default=timezone.now())
    payment_amount = models.FloatField(verbose_name='Сумма платежа')
    payment_method = models.CharField(max_length=20, verbose_name='Способ платежа', choices=PAYMENT_CHOICES,
                                      default='cash')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Пользователь',
                             **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='paid', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING, related_name='paid', **NULLABLE)

    def __str__(self):
        return f'{self.course if self.course and not self.lesson else self.lesson}, оплачено {self.payment_amount} руб'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-payment_date',)