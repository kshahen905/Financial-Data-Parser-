import unittest
import pandas as pd
from src.core.data_type_detector import DataTypeDetector

class TestDataTypeDetector(unittest.TestCase):
    def setUp(self):
        self.detector = DataTypeDetector()

    def test_detect_date_format_ymd(self):
        series = pd.Series(["2023-01-01", "2022-12-31", "2024-03-15"])
        result = self.detector.analyze_column(series)
        self.assertEqual(result, "date")

    def test_detect_date_format_dmy(self):
        series = pd.Series(["01/01/2023", "31/12/2022", "15/03/2024"])
        result = self.detector.analyze_column(series)
        self.assertEqual(result, "date")

    def test_detect_numeric(self):
        series = pd.Series(["1000", "$2,500.50", "₹3,000", "(4500)", "1.25", "€2,000"])
        result = self.detector.analyze_column(series)
        self.assertEqual(result, "number")

    def test_detect_string(self):
        series = pd.Series(["hello", "world", "apple", "banana"])
        result = self.detector.analyze_column(series)
        self.assertEqual(result, "string")

    def test_mixed_data_defaults_to_string(self):
        series = pd.Series(["hello", "100", "2023-01-01", "random"])
        result = self.detector.analyze_column(series)
        self.assertEqual(result, "string")  # Not 80% number or date

    def test_empty_series(self):
        series = pd.Series([])
        result = self.detector.analyze_column(series)
        self.assertEqual(result, "unknown")

    def test_nan_only_series(self):
        series = pd.Series([None, None, float("nan")])
        result = self.detector.analyze_column(series)
        self.assertEqual(result, "unknown")

if __name__ == '__main__':
    unittest.main()
