import os
import sys
import pandas as pd

# Add project root to sys.path (for execution, optional)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, ROOT_DIR)

# Updated imports using src.*
from src.core.excel_processor import ExcelProcessor
from src.core.data_type_detector import DataTypeDetector
from src.core.format_parser import FormatParser
from src.core.data_storage import DataStorage
from config import settings

file = os.path.join(settings.DATA_DIR, settings.EXCEL_FILES[0])

processor = ExcelProcessor()
processor.load_files([file])

detector = DataTypeDetector()
parser = FormatParser()
storage = DataStorage()

for path, sheets in processor.files.items():
    for name, df in sheets.items():
        col_types = {col: detector.analyze_column(df[col]) for col in df.columns}
        for col, typ in col_types.items():
            if typ == "number":
                df[col] = df[col].apply(parser.parse_amount)
            elif typ == "date":
                df[col] = df[col].apply(parser.parse_date)
        storage.store_data(f"{path}:{name}", df, col_types)

print(" Successfully loaded and parsed data.")
