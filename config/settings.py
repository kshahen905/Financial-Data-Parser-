import os

# Root path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Folder that contains your Excel files
DATA_DIR = os.path.join(BASE_DIR, "data", "sample")

# List of Excel file names (relative to sample folder)
EXCEL_FILES = [
    "C:/Users/Hp/Downloads/financial-data-parser (1)/financial-data-parser/data/sample/KH_Bank.XLSX",
    "C:/Users/Hp/Downloads/financial-data-parser (1)/financial-data-parser/data/sample/Customer_Ledger_Entries_FULL.xlsx"
]

# Add these for parsing
DATE_FORMATS = [
    "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%b-%Y",
    "%b %Y", "%b-%y", "%d-%m-%Y", "%Y/%m/%d"
]

NUMERIC_THRESHOLD = 0.8
