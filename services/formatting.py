from django.core.exceptions import ValidationError


def data_formatting(value: str, is_name=False) -> str:
    if value and value.strip():
        value = value.strip().capitalize() if is_name else value.strip()
    else:
        raise ValidationError("This field is required and should not be just spaces.")

    return value
