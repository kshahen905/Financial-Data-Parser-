import re

def clean_string(val: str) -> str:
    """Convert to lowercase, remove special chars, and trim spaces."""
    if not isinstance(val, str):
        return str(val)
    return re.sub(r"[^a-zA-Z0-9_]+", "_", val.strip().lower())

def safe_float(val) -> float:
    """Try converting to float; return None if fails."""
    try:
        return float(str(val).replace(",", "").replace("(", "-").replace(")", ""))
    except (ValueError, TypeError):
        return None

def safe_strip(val):
    """Strip strings or return original."""
    return val.strip() if isinstance(val, str) else val
