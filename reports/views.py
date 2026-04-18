from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404

from jobs.models import JobLog
from .forms import DynamicReportForm
from .models import ReportConfiguration
from .report_library import ReportLibrary
from django.shortcuts import render, get_object_or_404
from .models import ReportConfiguration
from reports import report_library  # модул, който съдържа всички функции

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
    rep_config = get_object_or_404(ReportConfiguration, slug=report_slug)
    result = None

    # Проверка дали има реални параметри
    has_params = any(request.GET.values())

    if has_params:
        form = DynamicReportForm(rep_config, request.GET)

        if form.is_valid():
            # Проверка дали функцията съществува
            method = getattr(ReportLibrary, rep_config.method_name, None)
            if not method:
                form.add_error(None, f"Report function '{rep_config.method_name}' not found.")
            else:
                try:
                    result = method(**form.cleaned_data)
                except Exception as e:
                    form.add_error(None, f"Error executing report: {str(e)}")
    else:
        form = DynamicReportForm(rep_config)

    return render(request, 'reports/report.html', {
        'form': form,
        'result': result,
        'config': rep_config,
        'page_title': 'Report',
    })





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

    # Извикваме функцията от reports library
    func = getattr(report_library, report.method_name)
    result = func(**params)

    return render(request, "reports/report_view.html", {
        "report": report,
        "columns": result["columns"],
        "rows": result["rows"],
        "chart": result.get("chart"),
    })




async def stats(request):
    total = await JobLog.objects.acount()
    latest = await JobLog.objects.select_related().order_by('job__job_code').afirst()
    j_response = JsonResponse({'total': total, 'latest': latest.job.job_code if latest else None}, status=200)
    return j_response