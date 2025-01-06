from django.core.exceptions import ValidationError


def data_formatting(value: str, is_name: bool = False, is_required_field: bool = True):
    """
    Formats the provided string value by stripping whitespace and capitalizing it if specified as a name.

    :param value: The string value to be formatted.
    :param is_name: If True, the value will be capitalized. Default is False.
    :param is_required_field: If True, raises ValidationError for empty or whitespace-only values. Default is True.
    :return: The formatted string value.
    :raises ValidationError: If is_required_field is True and the value is empty or contains only whitespace.
    """
    if value and value.strip():
        return value.strip().capitalize() if is_name else value.strip()
    else:
        if is_required_field:
            raise ValidationError("This field is required and should not be just spaces.")
    return value.strip()
