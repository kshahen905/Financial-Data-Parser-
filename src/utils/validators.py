import re
import pandas as pd

def is_numeric_string(val: str) -> bool:
    """Check if string looks like a number (e.g., 1,234.56 or (500))"""
    if not isinstance(val, str):
        return False
    return bool(re.match(r"^-?[\(]?\d[\d,\.]*[\)]?$", val.strip()))

def is_valid_date_string(val: str) -> bool:
    """Roughly check if a value could be a date string."""
    if not isinstance(val, str):
        return False
    return bool(re.search(r"\d{4}|\d{1,2}/\d{1,2}", val))

def has_required_columns(df: pd.DataFrame, required_cols: list) -> bool:
    """Check if required columns exist in the DataFrame"""
    return all(col in df.columns for col in required_cols)

def is_empty_cell(val) -> bool:
    """Check if a cell is empty or null."""
    return pd.isna(val) or str(val).strip() == ""
