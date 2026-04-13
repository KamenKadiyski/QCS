from django.core.exceptions import ValidationError


def min_value_validator(value):
    if value <= 0:
        raise ValidationError('Value must be greater than zero.')