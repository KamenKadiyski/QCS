from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Material, Additive


# Create your views here.
class MaterialListView(ListView):
    model = Material
    template_name = 'materials/list_materials.html'
    page_title = 'List of Materials'
    def get_queryset(self):
        return Material.objects.all().order_by('name').select_related('supplier')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'page_title': self.page_title,
            }
        )
        return context


class AddMaterialView(CreateView):
    model = Material
    fields = '__all__'
    template_name = 'materials/add_material.html'
    success_url = reverse_lazy('materials:list_materials')
    page_title = 'Add Material'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control shadow-sm'})
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'page_title': self.page_title,
            }
        )
        return context

class UpdateMaterialView(UpdateView):
    model = Material
    fields = '__all__'
    template_name = 'materials/update_material.html'
    success_url = reverse_lazy('materials:list_materials')
    page_title = 'Update Material'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control shadow-sm'})
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'page_title': self.page_title,
            }
        )
        return context





class AdditiveListView(ListView):
    model = Additive
    template_name = 'additives/list_additives.html'
    page_title = 'List of Additives'

    def get_queryset(self):
        return Additive.objects.all().order_by('name').select_related('supplier')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': self.page_title,
        })
        return context


class AddAdditiveView(CreateView):
    model = Additive
    fields = '__all__'
    template_name = 'additives/add_additive.html'
    success_url = reverse_lazy('materials:list_additives')
    page_title = 'Add Additive'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control shadow-sm'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': self.page_title,
        })
        return context


class UpdateAdditiveView(UpdateView):
    model = Additive
    fields = '__all__'
    template_name = 'additives/update_additive.html'
    success_url = reverse_lazy('materials:list_additives')
    page_title = 'Update Additive'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control shadow-sm'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': self.page_title,
        })
        return context
