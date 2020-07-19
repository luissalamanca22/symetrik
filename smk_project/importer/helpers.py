""""""
from django.utils import timezone
from django.utils.text import slugify

def clean_text(value):
    if not value or not isinstance(value, str):
        raise ValueError("You have to provide a string value")
    return slugify(value).replace("-", "_")

def format_filename_as_tablename(value):
    return "{}_{}".format(clean_text(value.partition(".")[0]), timezone.now().strftime("%d%m%Y"))