from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404

from jobs.models import JobLog
from .forms import DynamicReportForm
from .models import ReportConfiguration
from .report_library import ReportLibrary


# Create your views here.


def report_list(request):
    page_title = 'Reports'


    reports = ReportConfiguration.objects.filter(is_active=True)
    context = {
        'reports': reports,
        'page_title': page_title,

    }
    return render(request, 'reports/reports_list.html', context)



def report_view(request: HttpRequest, report_slug: str) -> HttpResponse:
    page_title = 'Report'


    rep_config = get_object_or_404(ReportConfiguration, slug=report_slug)
    result = None
    if  request.GET:
        form = DynamicReportForm(rep_config, request.POST or request.GET)
        if form.is_valid():
            method = getattr(ReportLibrary, rep_config.method_name)
            result = method(**form.cleaned_data)
    else:
        form = DynamicReportForm(rep_config)
    context = {
        'form': form,
        'result': result,
        'config' : rep_config,
        'page_title': page_title,


    }

    return render(request, 'reports/report.html', context)



async def stats(request):
    total = await JobLog.objects.acount()
    latest = await JobLog.objects.select_related().order_by('job__job_code').afirst()
    j_response = JsonResponse({'total': total, 'latest': latest.job.job_code if latest else None}, status=200)
    return j_response