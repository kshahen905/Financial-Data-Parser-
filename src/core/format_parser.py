import re
import pandas as pd
from datetime import datetime, timedelta

class FormatParser:
    def __init__(self):
        pass

    def parse_amount(self, value):
        if isinstance(value, (int, float)):
            return float(value)

        val = str(value).strip()
        if val == "":
            return None

        val = val.replace("(", "-").replace(")", "")  # Negative format
        val = re.sub(r"[^\d\.\-KkMmBb]", "", val)     # Remove symbols

        multiplier = 1
        if val[-1:].lower() == "k":
            multiplier = 1_000
            val = val[:-1]
        elif val[-1:].lower() == "m":
            multiplier = 1_000_000
            val = val[:-1]
        elif val[-1:].lower() == "b":
            multiplier = 1_000_000_000
            val = val[:-1]

        try:
            return float(val) * multiplier
        except:
            return None

    def parse_date(self, value):
        if pd.isna(value):
            return None

        if isinstance(value, datetime):
            return value

        try:
            val = float(value)
            if 30000 < val < 50000:
                return datetime(1899, 12, 30) + timedelta(days=val)
        except:
            pass

        val = str(value).strip()
        formats = [
            "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%b-%Y",
            "%b %Y", "%b-%y", "%d-%m-%Y", "%Y/%m/%d"
        ]
        for fmt in formats:
            try:
                return datetime.strptime(val, fmt)
            except:
                continue

        return None

# Test block so you can run this file directly
if __name__ == "__main__":
    parser = FormatParser()

    print("Amount Tests:")
    print(parser.parse_amount("₹1,23,456.78"))     # 123456.78
    print(parser.parse_amount("(2,500.00)"))       # -2500.0
    print(parser.parse_amount("1.2M"))             # 1200000.0
    print(parser.parse_amount("$1234.56"))         # 1234.56

    print("\nDate Tests:")
    print(parser.parse_date("2023-12-31"))         # datetime object
    print(parser.parse_date("44927"))              # Excel serial → 2023-01-01
    print(parser.parse_date("Mar 2024"))           # datetime object
