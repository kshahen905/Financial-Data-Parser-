import os
import sys
import time
import pandas as pd

# Add project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, ROOT_DIR)

from src.core.format_parser import FormatParser

df = pd.DataFrame({"Amount": ["1.5M"] * 10000})
parser = FormatParser()

start = time.time()
df["Parsed"] = df["Amount"].apply(parser.parse_amount)
end = time.time()

print(f" Parsed 10,000 rows in {end - start:.2f} seconds")
