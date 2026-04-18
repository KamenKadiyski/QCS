from django import forms
from django.apps import apps

class DynamicReportForm(forms.Form):
    def __init__(self, report_configuration, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for parameter in report_configuration.parameters.all():
            field_kwargs = {
                "label": parameter.label,
                "required": parameter.is_required,
            }

            # DATE FIELD
            if parameter.parameter_type == "date":
                self.fields[parameter.name] = forms.DateField(
                    widget=forms.DateInput(attrs={"type": "date"}),
                    **field_kwargs
                )

            # CHOICE FIELD (Динамичен от Модел)
            elif parameter.parameter_type == "choice" and parameter.source_model:
                try:
                    app_label, model_name = parameter.source_model.split(".")
                    Model = apps.get_model(app_label, model_name)
                    queryset = Model.objects.all().order_by("id")
                    self.fields[parameter.name] = forms.ModelChoiceField(
                        queryset=queryset, empty_label="---", **field_kwargs
                    )
                except Exception:
                    self.fields[parameter.name] = forms.CharField(disabled=True, initial="Error loading model")

            # STATIC CHOICE FIELD (За материалите)
            elif parameter.parameter_type == "static_choice":
                choices = [('', '--- All Types ---')]
                if parameter.name == "material_type":
                    choices += [
                        ('block', 'PPC (Block Copolymer)'),
                        ('clear', 'Clear PPR (Random Copolymer)'),
                        ('homopolymer', 'PPH (Homopolymer)'),
                        ('other', 'Other'),
                    ]
                self.fields[parameter.name] = forms.ChoiceField(choices=choices, **field_kwargs)

            # INTEGER FIELD
            elif parameter.parameter_type == "int":
                self.fields[parameter.name] = forms.IntegerField(**field_kwargs)

            # BOOLEAN FIELD
            elif parameter.parameter_type == "bool":
                self.fields[parameter.name] = forms.BooleanField(
                    required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
                )
                continue # Скипваме долния клас за буутстрап

            # DEFAULT STRING
            else:
                self.fields[parameter.name] = forms.CharField(**field_kwargs)

        # Bootstrap Styling
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-control"})
