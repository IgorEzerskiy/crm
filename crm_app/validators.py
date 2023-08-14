import re

from django.core.exceptions import ValidationError


def email_validator(email):
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):
        raise ValidationError('Enter a valid email address.')
