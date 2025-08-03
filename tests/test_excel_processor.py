import unittest
from unittest.mock import patch, MagicMock
from src.core.excel_processor import ExcelProcessor

class TestExcelProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ExcelProcessor()

    @patch("pandas.read_excel")
    def test_load_files_success(self, mock_read_excel):
        # Mock read_excel to return fake sheets
        mock_read_excel.return_value = {
            "Sheet1": MagicMock(shape=(10, 3), columns=["A", "B", "C"]),
            "Sheet2": MagicMock(shape=(5, 2), columns=["X", "Y"])
        }

        test_paths = ["fake_file_1.xlsx", "fake_file_2.xlsx"]
        self.processor.load_files(test_paths)

        self.assertIn("fake_file_1.xlsx", self.processor.files)
        self.assertIn("fake_file_2.xlsx", self.processor.files)
        self.assertEqual(len(self.processor.files["fake_file_1.xlsx"]), 2)

    @patch("pandas.read_excel", side_effect=Exception("File not found"))
    def test_load_files_error(self, mock_read_excel):
        test_paths = ["nonexistent_file.xlsx"]
        self.processor.load_files(test_paths)

        # Should not crash, and file should not be added
        self.assertNotIn("nonexistent_file.xlsx", self.processor.files)

    def test_get_sheet_info_output(self):
        self.processor.files = {
            "test.xlsx": {
                "Sheet1": MagicMock(shape=(10, 3), columns=["A", "B", "C"]),
                "Sheet2": MagicMock(shape=(5, 2), columns=["X", "Y"]),
            }
        }

        # Just ensure it prints without error
        try:
            self.processor.get_sheet_info()
        except Exception as e:
            self.fail(f"get_sheet_info() raised an exception: {e}")

    def test_preview_data_output(self):
        self.processor.files = {
            "test.xlsx": {
                "Sheet1": MagicMock(head=MagicMock(return_value="Data Preview")),
            }
        }

        # Just ensure it prints preview without error
        try:
            self.processor.preview_data()
        except Exception as e:
            self.fail(f"preview_data() raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
