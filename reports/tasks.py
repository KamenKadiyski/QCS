import calendar
from datetime import datetime

from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Sum
from django.utils import timezone

from jobs.models import JobLog, ScrapLog


@shared_task
def job_log_mail_notification(job_code):
    send_mail(
        subject='New job',
        message=f'A new job {job_code} was created',
        from_email='system_log@wathmoreuk.com',
        recipient_list=['Steve.Box@whatmore.com','Matt.Hand@whatmore.com'],
    )



@shared_task
def scrap_persent_mail_notification(job_log_id, job_code):
    order_amount = JobLog.objects.filter(id=job_log_id).first().order_total_amount or 0
    scrapped_amount = ScrapLog.objects.filter(job_log_id=job_log_id).aggregate(Sum('amount_scrap'))['amount_scrap__sum'] or 0
    scrap_percent = round((scrapped_amount / order_amount) * 100, 2) if order_amount > 0 else 0
    if scrap_percent > 1:
        send_mail(
            subject='Scrap alert',
            message=f'The scrap level exceeds the specified percentage. For more information, '
                    f'please visit: http://127.0.0.1:8000/reports/scrap_job/?job_code={job_code}',
            from_email='system_log@wathmoreuk.com',
            recipient_list=['Steve.Box@whatmore.com','Matt.Hand@whatmore.com'],
        )


@shared_task
def check_monthly_scrap_rate():
    now = timezone.now()

    first_day = timezone.make_aware(datetime(now.year, now.month, 1, 0, 0, 0))

    _, last_day_num = calendar.monthrange(now.year, now.month)
    last_day = timezone.make_aware(datetime(now.year, now.month, last_day_num, 23, 59, 59))

    scrapped_amount = ScrapLog.objects.filter(date_and_time__range=(first_day, last_day)).aggregate(Sum('amount_scrap'))['amount_scrap__sum'] or 0
    order_amount = JobLog.objects.filter(date_and_time__range=(first_day, last_day)).aggregate(Sum('order_total_amount'))['order_total_amount__sum'] or 0


    total_produced = order_amount + scrapped_amount
    scrap_percent = round((scrapped_amount / total_produced) * 100, 2) if total_produced > 0 else 0

    if scrap_percent > 0:
        send_mail(
            subject='Monthly scrap rate',
            message=(
                f'Hello,\n\n'
                f'The current scrap rate is: {scrap_percent}%\n'
                f'Total monthly order amount: {order_amount} pcs\n'
                f'Total monthly scrap: {scrapped_amount} pcs\n'
                f'Total produced: {total_produced} pcs'
            ),
            from_email='system_log@wathmoreuk.com',
            recipient_list=['Steve.Box@whatmore.com','Matt.Hand@whatmore.com'],
        )


from datetime import timedelta



@shared_task
def check_15min_scrap_rate():
    now = timezone.now()
    # Дефиниране на началната точка (преди 15 минути)
    fifteen_minutes_ago = now - timedelta(minutes=15)

    # Изчисляване на количествата само за последните 15 минути
    scrapped_amount = ScrapLog.objects.filter(
        date_and_time__range=(fifteen_minutes_ago, now)
    ).aggregate(Sum('amount_scrap'))['amount_scrap__sum'] or 0

    order_amount = JobLog.objects.filter(
        date_and_time__range=(fifteen_minutes_ago, now)
    ).aggregate(Sum('order_total_amount'))['order_total_amount__sum'] or 0

    # Изчисляване на процента брак за интервала
    total_produced = order_amount + scrapped_amount
    scrap_percent = round((scrapped_amount / total_produced) * 100, 2) if total_produced > 0 else 0

    # Изпращане на имейл, ако има регистриран брак в този интервал
    if scrap_percent > 0:
        send_mail(
            subject='15-Minute Scrap Rate Alert',
            message=(
                f'Hello,\n\n'
                f'The scrap rate for the last 15 minutes is: {scrap_percent}%\n'
                f'Order amount (last 15m): {order_amount} pcs\n'
                f'Scrap amount (last 15m): {scrapped_amount} pcs\n'
                f'Total produced (last 15m): {total_produced} pcs'
            ),
            from_email='system_log@wathmoreuk.com',
            recipient_list=['Steve.Box@whatmore.com', 'Matt.Hand@whatmore.com'],
        )
