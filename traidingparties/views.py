from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Supplier, DeliveryQualityIssue


# Create your views here.
class SupplierCreatView(CreateView):
    model = Supplier
    fields = '__all__'
    template_name = 'traidingparties/add_supplier.html'
    success_url = reverse_lazy('traidingparties:add_supplier')
    page_title = 'Add Supplier'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control shadow-sm'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all().order_by('name')
        context['page_title'] = self.page_title
        return context


class SupplierUpdateView(UpdateView):
    model = Supplier
    fields = '__all__'
    template_name = 'traidingparties/update_supplier.html'
    success_url = reverse_lazy('traidingparties:add_supplier')
    page_title = 'Update Supplier'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control shadow-sm'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['suppliers'] = Supplier.objects.all().order_by('name')
        context['page_title'] = self.page_title
        return context






class DeliveryQualityIssueCreateView(CreateView):
    model = DeliveryQualityIssue
    fields = ['supplier', 'material', 'additive', 'bach_number', 'issue_description']
    template_name = 'traidingparties/add_delivery_issue.html'
    success_url = reverse_lazy('traidingparties:add_delivery_issue') # Връща се на същата страница
    page_title = 'Report Delivery Quality Issue'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control shadow-sm'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = DeliveryQualityIssue.objects.all().order_by('-issue_date').select_related(
            'supplier', 'material', 'additive'
        )
        context['page_title'] = self.page_title
        return context
