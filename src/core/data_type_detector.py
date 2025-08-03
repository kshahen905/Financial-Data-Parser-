import pandas as pd
import numpy as np
from datetime import datetime

class DataTypeDetector:
    def __init__(self):
        pass

    def analyze_column(self, series: pd.Series) -> str:
        data = series.dropna().astype(str).head(50)

        if data.empty:
            return "unknown"

        # Try to detect date
        date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%b %Y", "%b-%y"]
        for val in data:
            for fmt in date_formats:
                try:
                    datetime.strptime(val.strip(), fmt)
                    return "date"
                except:
                    continue

        # Try to detect number (remove symbols like $, %, ,)
        def is_number(val):
            try:
                float(str(val).replace(",", "").replace("$", "").replace("€", "").replace("₹", "").replace("(", "-").replace(")", ""))
                return True
            except:
                return False

        if data.map(is_number).mean() > 0.8:  # 80% of values should be numeric
            return "number"

        return "string"
