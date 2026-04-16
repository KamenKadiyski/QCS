import time

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def job_log_mail_notification(job_code):
    send_mail(
        subject='New job',
        message=f'A new job {job_code} was created',
        from_email='system_log@wathmoreuk.com',
        recipient_list=['steve.box@whatmore.com'],
    )