from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from users.models import Subscription, User


@shared_task
def send_update_info_task(course_id, subject, message):
    """Функция отправки сообщения об обновлении курса"""
    subscription_list = Subscription.objects.filter(course_id=course_id)
    for subs in subscription_list:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subs.user.email],
            fail_silently=False
        )


@shared_task
def check_user_activity_task():
    """Функция проверки активности пользователя"""
    users_list = User.objects.filter(is_active=True, is_superuser=False, last_login__isnull=False)

    for user in users_list:
        if user.last_login < (timezone.now() - timedelta(days=30)):
            user.is_active = False
            user.save()