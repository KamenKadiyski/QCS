from django.db.models import Sum

from jobs.models import JobLog, ScrapLog


def scrap_job_report(job_code, **kwargs):

    joblogs = (
        JobLog.objects
        .filter(job__job_code=job_code)
        .annotate(total_scrap=Sum('scraps__amount_scrap'))
        .order_by('-date_and_time')
    )

    rows = []
    scrap_values = []
    amount_values = []
    labels = []

    for jlog in joblogs:
        total_scrap = jlog.total_scrap or 0
        amount = jlog.order_total_amount or 0

        # Scrap %
        scrap_percent = round((total_scrap / amount) * 100, 2) if amount > 0 else 0

        rows.append({
            "Job Log ID": jlog.id,
            "Date": jlog.date_and_time.strftime("%Y-%m-%d %H:%M"),
            "Material": jlog.current_material.name,
            "Tool": jlog.current_tool.code,
            "Machine": jlog.current_machine.machine_number,
            "Job amount": amount,
            "Total Scrap": total_scrap,
            "Scrap %": scrap_percent,
        })

        labels.append(jlog.date_and_time.strftime("%Y-%m-%d %H:%M"))
        scrap_values.append(total_scrap)
        amount_values.append(amount)

    chart = {
        'labels': labels,
        'datasets': [
            {
                'label': 'Total Scrap',
                'data': scrap_values,
                'backgroundColor': 'rgba(255, 99, 132, 0.6)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Job amount',
                'data': amount_values,
                'backgroundColor': 'rgba(54, 162, 235, 0.6)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            }
        ]
    }

    return {
        'columns': [
            'Job Log ID',
            'Date',
            'Material',
            'Tool',
            'Machine',
            'Job amount',
            'Total Scrap',
            'Scrap %'
        ],
        'rows': rows,
        'chart': chart
    }


def scrap_report_comparing_materials(start_date, end_date,material_type):
    scrap_logs = ScrapLog.objects.all()
    if material_type != 'All':
        if material_type:
            scrap_logs = scrap_logs.filter(job_log__current_material__type=material_type)
    if start_date:
            scrap_logs = scrap_logs.filter(date_and_time__gte=start_date)
    if end_date:
            scrap_logs = scrap_logs.filter(date_and_time__lte=end_date)

    scrap_logs = scrap_logs.values('job_log__current_material__name').annotate(
            total_scrap=Sum('amount_scrap')
        ).order_by('job_log__current_material__type')


    rows = []
    scrap_values = []
    labels = []
    colours = [
    'rgba(0, 102, 204, 1)',    # Кралско синьо
    'rgba(255, 102, 102, 1)',  # Корал
    'rgba(0, 153, 76, 1)',     # Тъмно зелено
    'rgba(204, 153, 255, 1)',  # Лавандула
    'rgba(255, 255, 102, 1)',  # Светло жълто
    'rgba(255, 0, 0, 1)',      # Чисто червено
    'rgba(0, 204, 204, 1)',    # Циан
    'rgba(153, 51, 102, 1)',   # Винено
    'rgba(255, 204, 153, 1)',  # Праскова
    'rgba(128, 128, 0, 1)',    # Маслинено
    'rgba(0, 0, 128, 1)',      # Тъмносин (Navy)
    'rgba(192, 192, 192, 1)',  # Сребристо
    'rgba(0, 255, 128, 1)',    # Пролетно зелено
    'rgba(102, 0, 204, 1)',    # Индиго
    'rgba(255, 102, 0, 1)',    # Наситено оранжево
    'rgba(0, 0, 0, 1)',         # Черно (за силен акцент)
    'rgba(0, 51, 102, 1)',      # Тъмно морско синьо (Deep Sea)
    'rgba(204, 0, 102, 1)',     # Рубинено червено
    'rgba(102, 255, 178, 1)',   # Светла мента
    'rgba(255, 215, 0, 1)',     # Златно
    'rgba(127, 255, 0, 1)',     # Шартрез (Зелено-жълто)


]

    dataset = []
    for slog in scrap_logs:
        rows.append({
            "Material": slog['job_log__current_material__name'],
            "Total Scrap": slog['total_scrap'],

        })

        labels.append(slog['job_log__current_material__name'])
        scrap_values.append(slog['total_scrap'])
        dataset.append({
            'label': slog['job_log__current_material__name'],
            'data': [slog['total_scrap']],
            'backgroundColor': colours[labels.index(slog['job_log__current_material__name']) % len(colours)],
            'borderWidth': 1

        })
    chart = {
        'labels': ['Total Scrap'],
        'datasets': dataset
    }
    return {
        'columns': [
            'Material',
            'Total Scrap',
        ],
        'rows': rows,
        'chart': chart
    }


def scrap_report_by_tool(start_date, end_date,tool_code=None):

    scrap_logs = ScrapLog.objects.all()

    if tool_code:
        scrap_logs = scrap_logs.filter(job_log__current_tool__code=tool_code)


    if start_date:
            scrap_logs = scrap_logs.filter(date_and_time__gte=start_date)
    if end_date:
            scrap_logs = scrap_logs.filter(date_and_time__lte=end_date)

    scrap_logs = scrap_logs.values('job_log__current_tool__code').annotate(
            total_scrap=Sum('amount_scrap')
        ).order_by('job_log__current_tool__code')


    rows = []
    scrap_values = []
    labels = []
    colours = [
        'rgba(0, 102, 204, 1)',  # Кралско синьо
        'rgba(255, 102, 102, 1)',  # Корал
        'rgba(0, 153, 76, 1)',  # Тъмно зелено
        'rgba(204, 153, 255, 1)',  # Лавандула
        'rgba(255, 255, 102, 1)',  # Светло жълто
        'rgba(255, 0, 0, 1)',  # Чисто червено
        'rgba(0, 204, 204, 1)',  # Циан
        'rgba(153, 51, 102, 1)',  # Винено
        'rgba(255, 204, 153, 1)',  # Праскова
        'rgba(128, 128, 0, 1)',  # Маслинено
        'rgba(0, 0, 128, 1)',  # Тъмносин (Navy)
        'rgba(192, 192, 192, 1)',  # Сребристо
        'rgba(0, 255, 128, 1)',  # Пролетно зелено
        'rgba(102, 0, 204, 1)',  # Индиго
        'rgba(255, 102, 0, 1)',  # Наситено оранжево
        'rgba(0, 0, 0, 1)',  # Черно (за силен акцент)
        'rgba(0, 51, 102, 1)',  # Тъмно морско синьо (Deep Sea)
        'rgba(204, 0, 102, 1)',  # Рубинено червено
        'rgba(102, 255, 178, 1)',  # Светла мента
        'rgba(255, 215, 0, 1)',  # Златно
        'rgba(127, 255, 0, 1)',  # Шартрез (Зелено-жълто)

    ]

    dataset = []
    for slog in scrap_logs:
        rows.append({
            "Tool": slog['job_log__current_tool__code'],
            "Total Scrap by tool": slog['total_scrap'],

        })

        labels.append(slog['job_log__current_tool__code'])
        scrap_values.append(slog['total_scrap'])
        dataset.append({
            'label': slog['job_log__current_tool__code'],
            'data': [slog['total_scrap']],
            'backgroundColor': colours[labels.index(slog['job_log__current_tool__code']) % len(colours)],
            'borderWidth': 1

        })
    chart = {
        'labels': ['Total Scrap'],
        'datasets': dataset
    }
    return {
        'columns': [
            'Tool',
            'Total Scrap by tool',
        ],
        'rows': rows,
        'chart': chart
    }


