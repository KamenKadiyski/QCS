from django.db.models import Sum, F
from jobs.models import JobLog, ScrapLog


class ReportLibrary:
    @staticmethod
    def scrap_compare(job_code):

        return ScrapLog.objects.filter(
            job_log__job__job_code=job_code
        ).select_related('job_log__job')
    @staticmethod
    def get_detailed_scrap_report(job_code):

        report_set = JobLog.objects.filter(
            job__job_code=job_code
        ).annotate(
            total_scrap=Sum('scraps__amount_scrap')
        ).order_by('-date_and_time')

        return report_set