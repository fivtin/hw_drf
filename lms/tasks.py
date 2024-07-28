from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from lms.models import CourseSubscriber, Course
from users.models import User


@shared_task
def send_email_for_course_update(course_id):
    course = Course.objects.get(pk=course_id)
    subscribers = CourseSubscriber.objects.filter(course=course_id)
    users = [subscriber.user.email for subscriber in subscribers]
    send_mail(
        subject='Обновление курса',
        message=f'В курсе "{course.title}" были обновления.',
        from_email=EMAIL_HOST_USER,
        recipient_list=users
    )


@shared_task
def block_inactive_users():
    users = User.objects.filter(is_active=True, last_login__lte=datetime.now() - timedelta(days=30))
    for user in users:
        user.is_active = False
        user.save()
