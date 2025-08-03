import os
import sys

# Add project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, ROOT_DIR)

from src.core.format_parser import FormatParser

parser = FormatParser()

amounts = ["$1,234.56", "(2,500.00)", "€1.234,56", "1.5M", "₹1,23,456"]
dates = ["12/31/2023", "2023-12-31", "Q4 2023", "Dec-23", "44927"]

print(" Amount Parsing:")
for a in amounts:
    print(f"{a} → {parser.parse_amount(a)}")

print("\n Date Parsing:")
for d in dates:
    print(f"{d} → {parser.parse_date(d)}")
