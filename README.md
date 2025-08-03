# Financial Data Parser

A modular Python application for parsing, analyzing, and querying financial data from Excel spreadsheets. Designed to handle complex formats, detect column data types, and provide clean, structured outputs for financial processing or reporting.

---

## Features

-  Load multiple Excel files (with multiple sheets)
-  Automatically detect column types: **date**, **number**, **string**
-  Parse currency formats (₹, $, €, K, M, B) and Excel serial dates
-  Query datasets with custom conditions (e.g., `Amount > 1000`)
-  Group and aggregate data (e.g., total by category or month)
-  Fully tested with `unittest`

---

## Project Structure

financial-data-parser/
├── main.py # Entry point
├── requirements.txt # Project dependencies
├── README.md # This file
├── src/ # Core logic
│ └── core/
│ ├── data_storage.py
│ ├── data_type_detector.py
│ ├── excel_processor.py
│ ├── format_parser.py
├── config/
│ └── settings.py # Excel file paths & data dir
├── tests/ # Unit tests for each core module
├── examples/ # Demo scripts: basic, advanced, performance
└── scripts/
└── run_benchmarks.py # Time benchmark for full pipeline


---

## Installation

Make sure you have Python 3.11+ installed.
git clone https://github.com/your-username/financial-data-parser.git
cd financial-data-parser
pip install -r requirements.txt

# How to Run
Run the full parser on your dataset:

--python main.py

# Expected output:

 Loading Excel Files...
 Processing Sheet: Sheet1 in KH_Bank.XLSX
 Example Query on Parsed Data
 KH_Bank.XLSX:Sheet1 → Amount > 1000

# Running Tests

Run all unit tests using:
python -m unittest discover -s tests
Each core module (data_storage, format_parser, etc.) is fully covered by tests.

# Sample Data Format

Your Excel sheets should contain financial columns such as:
Date, Amount, Category, Description
Amounts like $1,234.56, (2,500.00), 1.5M, etc.
Dates like 2023-12-31, 31/12/2023, or Excel serials like 44927

# Dependencies

Main libraries used:
pandas – data loading and processing
openpyxl – Excel file reader
datetime, re – date and text parsing
unittest – test framework

