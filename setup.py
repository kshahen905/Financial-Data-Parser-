# Required libraries 
import pandas as pd
import openpyxl
import numpy as np
import sqlite3
import re
from datetime import datetime
from decimal import Decimal
import locale


def check_environment():
    print("Pandas version:", pd.__version__)
    print("Openpyxl version:", openpyxl.__version__)
    print("NumPy version:", np.__version__)

if __name__ == "__main__":
    check_environment()
