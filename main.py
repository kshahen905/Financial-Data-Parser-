import os
import sys
import pandas as pd

# Add root to sys.path (only if needed for VS Code execution)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Import using src.core style
from src.core.excel_processor import ExcelProcessor
from src.core.data_type_detector import DataTypeDetector
from src.core.format_parser import FormatParser
from src.core.data_storage import DataStorage
from config import settings

# Prepare Excel file paths
data_files = [os.path.join(settings.DATA_DIR, f) for f in settings.EXCEL_FILES]

# Load Excel files
print("\n Loading Excel Files...")
processor = ExcelProcessor()
processor.load_files(data_files)
processor.get_sheet_info()

# Detect column types, parse, and store
detector = DataTypeDetector()
parser = FormatParser()
storage = DataStorage()

for path, sheets in processor.files.items():
    for sheet_name, df in sheets.items():
        print(f"\n🔍 Processing Sheet: {sheet_name} in {os.path.basename(path)}")

        col_types = {}
        for col in df.columns:
            col_type = detector.analyze_column(df[col])
            col_types[col] = col_type

            if col_type == "number":
                df[col] = df[col].apply(lambda x: parser.parse_amount(x) if pd.notna(x) else None)
            elif col_type == "date":
                df[col] = df[col].apply(lambda x: parser.parse_date(x) if pd.notna(x) else None)

        dataset_name = f"{os.path.basename(path)}:{sheet_name}"
        storage.store_data(dataset_name, df, col_types)

# Example Query
print("\n Example Query on Parsed Data")
for name in storage.datasets:
    amount_cols = storage.indexes[name]["amount_cols"]
    if amount_cols:
        print(f"\n {name} → {amount_cols[0]} > 1000")
        result = storage.query(name, amount_cols[0], lambda x: x and x > 1000)
        print(result.head())
        break
