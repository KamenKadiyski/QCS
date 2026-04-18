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
    latest = await JobLog.objects.select_related().order_by('job__job_code').afirst()
    j_response = JsonResponse({'total': total, 'latest': latest.job.job_code if latest else None}, status=200)
    return j_response


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

    # Събираме параметрите от request.GET
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




