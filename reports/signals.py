from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from jobs.models import JobLog

from reports.tasks import job_log_mail_notification

@receiver(post_save, sender=JobLog)
def create_job_log_report(sender, instance, created, **kwargs):
    if created:
        job_log_mail_notification.delay(instance.job.job_code)


