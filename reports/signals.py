from django.db.models.signals import post_save
from django.dispatch import receiver

from jobs.models import JobLog, ScrapLog
from reports.tasks import job_log_mail_notification, scrap_persent_mail_notification


@receiver(post_save, sender=JobLog)
def create_job_log_report(sender, instance, created, **kwargs):
    if created:
        job_log_mail_notification.delay(instance.job.job_code)


@receiver(post_save, sender=ScrapLog)
def create_scrap_log_report(sender, instance, created, **kwargs):
    if created:
        scrap_persent_mail_notification(instance.job_log_id, instance.job_log.job.job_code)