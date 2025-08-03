import unittest
from datetime import datetime
from src.core.format_parser import FormatParser

class TestFormatParser(unittest.TestCase):
    def setUp(self):
        self.parser = FormatParser()

    # -------- Amount Parsing Tests -------- #

    def test_parse_amount_simple_number(self):
        self.assertEqual(self.parser.parse_amount("1234.56"), 1234.56)

    def test_parse_amount_with_currency_and_commas(self):
        self.assertEqual(self.parser.parse_amount("$1,234.56"), 1234.56)
        self.assertEqual(self.parser.parse_amount("₹1,23,456.78"), 123456.78)

    def test_parse_amount_negative_in_parentheses(self):
        self.assertEqual(self.parser.parse_amount("(2,500.00)"), -2500.00)

    def test_parse_amount_suffixes(self):
        self.assertEqual(self.parser.parse_amount("1.2K"), 1200.0)
        self.assertEqual(self.parser.parse_amount("1.5M"), 1500000.0)
        self.assertEqual(self.parser.parse_amount("2B"), 2000000000.0)

    def test_parse_amount_invalid(self):
        self.assertIsNone(self.parser.parse_amount("Not a number"))

    def test_parse_amount_empty(self):
        self.assertIsNone(self.parser.parse_amount(""))

    def test_parse_amount_already_numeric(self):
        self.assertEqual(self.parser.parse_amount(5000), 5000.0)

    # -------- Date Parsing Tests -------- #

    def test_parse_date_standard_formats(self):
        self.assertEqual(self.parser.parse_date("2023-12-31"), datetime(2023, 12, 31))
        self.assertEqual(self.parser.parse_date("31/12/2023"), datetime(2023, 12, 31))
        self.assertEqual(self.parser.parse_date("12/31/2023"), datetime(2023, 12, 31))

    def test_parse_date_month_year(self):
        self.assertEqual(self.parser.parse_date("Mar 2024"), datetime(2024, 3, 1))

    def test_parse_date_serial(self):
        # Excel serial date 44927 → 2023-01-01
        self.assertEqual(self.parser.parse_date("44927"), datetime(2023, 1, 1))

    def test_parse_date_invalid(self):
        self.assertIsNone(self.parser.parse_date("Not a date"))

    def test_parse_date_already_datetime(self):
        dt = datetime(2022, 5, 1)
        self.assertEqual(self.parser.parse_date(dt), dt)

    def test_parse_date_nan(self):
        self.assertIsNone(self.parser.parse_date(float("nan")))

if __name__ == "__main__":
    unittest.main()
