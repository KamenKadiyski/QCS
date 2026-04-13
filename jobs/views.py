from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from jobs.forms import CreateJobForm, AddToJobLogForm
from jobs.models import Job, JobLog, ScrapReason, ScrapLog


# Create your views here.
class CreateJobView(CreateView):
    model = Job
    form_class = CreateJobForm
    template_name = 'jobs/create_job.html'
    success_url = reverse_lazy('jobs:list_jobs')
    page_title = 'Add details for the job'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'page_title': self.page_title,


            }
        )
        return context

class JobListView(ListView):
    model = Job
    template_name = 'jobs/list_jobs.html'
    page_title='List of Jobs'

    def get_queryset(self):
        jobs = Job.objects.all().order_by('job_code')
        return jobs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_items = [{
            'title': 'Add job',
            'url': reverse('jobs:create_job'),
            'icon': 'journal-check',
            'color': 'text-primary'
        }, {
            'title': 'Home',
            'url': reverse('accounts:home'),
            'icon': 'briefcase',
            'color': 'text-primary'
        }]
        context.update(
            {
                'page_title': self.page_title,
                'menu_items': menu_items,
            }
        )
        return context






class UpdateJobView(UpdateView):
    model = Job
    fields = '__all__'
    template_name = 'jobs/update_job.html'
    success_url = reverse_lazy('jobs:list_jobs')


class DeleteJobView(DeleteView):
    model = Job

    success_url = reverse_lazy('jobs:list_jobs')


class JobDetailsView(DetailView):
    model = Job
    template_name = 'jobs/job_details.html'
    page_title = 'Job Details'

    def get_object(self, queryset=None):
        job_id = self.kwargs.get('pk')
        return get_object_or_404(Job, pk=job_id)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_items = [{
            'title': 'Edit job',
            'url': reverse('jobs:update_job', kwargs={'pk': self.object.pk}),
            'icon': 'journal-check',
            'color': 'text-primary'
        }, {
            'title': 'Delete job',
            'url': reverse('jobs:delete_job', kwargs={'pk': self.object.pk}),
            'icon': 'dangerous',
            'color': 'text-primary'
        },
            {
                'title': 'Back to list',
                'url': reverse('jobs:list_jobs',),
                'icon': 'arrow-left',
                'color': 'text-primary'
            }
        ]
        context.update(
            {
                'page_title': self.page_title,
                'menu_items': menu_items,
            }
        )
        return context



class JobLogCreateView(CreateView):
        model = JobLog

        template_name = 'jobs/create_job_log.html'
        form_class = AddToJobLogForm
        success_url = reverse_lazy('jobs:list_jobs_logs')
        page_title = 'Create Job Log'


        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context.update(
                {
                    'page_title': self.page_title,

                }
            )
            return context


class JobLogListView(ListView):
    model = JobLog
    template_name = 'jobs/list_job_logs.html'
    page_title = 'List of Job Logs'
    def get_queryset(self):
        return JobLog.objects.select_related('job', 'current_material', 'current_additive', 'current_tool', 'current_machine').all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'page_title': self.page_title},

        )
        return context
class ScrapReasonAddView(CreateView):
        model = ScrapReason
        fields = '__all__'
        template_name = 'jobs/add_scrap_reason.html'
        success_url = reverse_lazy('jobs:add_scrap_reason')
        page_title = 'Add Scrap Reason'



        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context.update({
                'page_title': self.page_title,
                'existing_reasons': ScrapReason.objects.all().order_by('-id'),  # Всички причини
            })
            return context



class ScrapLogAddView(CreateView):
    model = ScrapLog
    fields = '__all__'
    template_name = 'jobs/add_scrap_log.html'
    success_url = reverse_lazy('jobs:add_scrap_log')
    page_title = 'Add Scrap Log'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Регистриране на Брак',
            'scrap_logs': ScrapLog.objects.select_related('job_log', 'scrap_reason').all().order_by('-date_and_time'),
        })
        return context




