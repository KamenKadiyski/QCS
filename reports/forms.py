from django import forms
from django.apps import apps




class DynamicReportForm(forms.Form):
    def __init__(self, report_configuration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for parameter in report_configuration.parameters.all():
            field_kwargs = {'label': parameter.label, 'required': parameter.is_required}
            if parameter.parameter_type == 'date':
                self.fields[parameter.name] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), **field_kwargs)
            elif parameter.parameter_type == 'choice' and parameter.source_model:
                Model = apps.get_model('your_app_label', parameter.source_model)
                self.fields[parameter.name] = forms.ModelChoiceField(queryset=Model.objects.all(), **field_kwargs)
            elif parameter.parameter_type == 'int':
                self.fields[parameter.name] = forms.IntegerField(**field_kwargs)
            else:
                self.fields[parameter.name] = forms.CharField(**field_kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})