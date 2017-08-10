import re
from django.core.validators import validate_email

def is_address(string):
    return re.match('^0[xX][a-fA-F\d]{40}$', string) is not None


def is_email(string):
    try:
        validate_email(string)
    except:
        return 0
    else:
        return 1
#    return re.match('.+@.+\..+', string) is not None


def is_percent(number):
    try:
        int(number)
    except ValueError:
        return False
    else:
        return 1 <= int(number) <= 100
