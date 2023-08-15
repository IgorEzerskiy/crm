import re

from django.core.exceptions import ValidationError


def email_validator(email):
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):
        raise ValidationError('Enter a valid email address.')


def telegram_username_validator(username):
    pattern = r'^@[a-zA-Z0-9._-]+$'

    if not re.match(pattern, username):
        raise ValidationError('Enter a valid telegram username.')
