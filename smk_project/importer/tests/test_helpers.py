from django.test import TestCase
from django.utils import timezone

from importer import helpers


class HelpersTestCase(TestCase):

    def test_clean_text_cleans_text_correctly(self):
        value = "&this-is-A-TEST_text$3232"
        cleaned_value = helpers.clean_text(value)
        self.assertEquals(cleaned_value, "this_is_a_test_text3232")

    def test_format_filename_as_tablename_formats_text_correctly(self):
        filename = "&this-is-A-TEST_text$3232.csv"
        expected_filename = "this_is_a_test_text3232_{}".format(
            timezone.now().strftime("%d%m%Y")
        )
        new_filename = helpers.format_filename_as_tablename(filename)
        self.assertEquals(new_filename, expected_filename)
