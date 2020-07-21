"""Functions that serve as utilities"""
from django.utils import timezone
from django.utils.text import slugify


def clean_text(value: str):
    """
    Removes all the special characters of the given text 
    and convert it to lowercase.
    :param value: Text to clean
    """
    if not value or not isinstance(value, str):
        raise ValueError("You have to provide a string value")
    return slugify(value).replace("-", "_")


def format_filename_as_tablename(filename: str):
    """
    Clean the given filename and add the current date at the end.
    :param filename: name of the file to format
    """
    try:
        return "{}_{}".format(clean_text(filename.partition(".")[0]), timezone.now().strftime("%d%m%Y"))
    except IndexError:
        raise ValueError("The given value is not a valid filename")
