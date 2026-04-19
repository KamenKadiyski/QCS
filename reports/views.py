from asgiref.sync import sync_to_async
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404

from jobs.models import JobLog
from .forms import DynamicReportForm
from .models import ReportConfiguration

from django.shortcuts import render, get_object_or_404
from .models import ReportConfiguration
from reports import report_library

# Create your views here.



async def stats(request):

    total = await JobLog.objects.acount()
    latest_obj = await JobLog.objects.select_related('job').order_by('-id').afirst()
    latest_code = latest_obj.job.job_code if latest_obj else None

    context = {
        'total': total,
        'latest': latest_code
    }


    return await sync_to_async(render)(request, 'reports/stats.html', context)




def report_list(request):
    page_title = 'Reports'


    reports = ReportConfiguration.objects.filter(is_active=True)
    context = {
        'reports': reports,
        'page_title': page_title,

    }
    return render(request, 'reports/reports_list.html', context)


def run_report(request, slug):
    report = get_object_or_404(ReportConfiguration, slug=slug)
    if not request.GET:
        return render(request, "reports/report_form.html", {"report": report})
    params = {}
    for p in report.parameters.all():
        value = request.GET.get(p.name)
        if p.is_required and not value:
            return render(request, "reports/report_form.html", {
                "report": report,
                "error": f"Missing required parameter: {p.label}"
            })
        params[p.name] = value
    func = getattr(report_library, report.method_name)
    result = func(**params)

    return render(request, "reports/report_view.html", {
        "report": report,
        "columns": result["columns"],
        "rows": result["rows"],
        "chart": result.get("chart"),
    })



