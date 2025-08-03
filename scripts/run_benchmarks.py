import os
import sys
import time
import pandas as pd

# Add project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, ROOT_DIR)

# Use src.core and config
from src.core.excel_processor import ExcelProcessor
from src.core.data_type_detector import DataTypeDetector
from src.core.format_parser import FormatParser
from src.core.data_storage import DataStorage
from config import settings

# Start benchmarking
start_time = time.time()

# Load Excel files
data_files = [os.path.join(settings.DATA_DIR, f) for f in settings.EXCEL_FILES]
processor = ExcelProcessor()
processor.load_files(data_files)

# Detect and parse
detector = DataTypeDetector()
parser = FormatParser()
storage = DataStorage()

for path, sheets in processor.files.items():
    for name, df in sheets.items():
        col_types = {col: detector.analyze_column(df[col]) for col in df.columns}
        for col, typ in col_types.items():
            if typ == "number":
                df[col] = df[col].apply(lambda x: parser.parse_amount(x) if pd.notna(x) else None)
            elif typ == "date":
                df[col] = df[col].apply(lambda x: parser.parse_date(x) if pd.notna(x) else None)

        dataset_name = f"{os.path.basename(path)}:{name}"
        storage.store_data(dataset_name, df, col_types)

# End benchmarking
end_time = time.time()
duration = end_time - start_time

print(f"\n Benchmark completed in {duration:.2f} seconds")
