import pandas as pd

class DataStorage:
    def __init__(self):
        self.datasets = {}       # Store original dataframes
        self.column_types = {}   # Store type info (date, amount, string)
        self.indexes = {}        # Optional: store fast lookup indexes

    def store_data(self, name: str, df: pd.DataFrame, column_types: dict):
        self.datasets[name] = df
        self.column_types[name] = column_types

        # Create basic indexes (can be extended)
        self.indexes[name] = {
            'date_cols': [col for col, typ in column_types.items() if typ == 'date'],
            'amount_cols': [col for col, typ in column_types.items() if typ == 'number'],
            'string_cols': [col for col, typ in column_types.items() if typ == 'string']
        }

    def query(self, name: str, column: str, condition_func):
        df = self.datasets.get(name)
        if df is not None and column in df.columns:
            return df[df[column].apply(condition_func)]
        return pd.DataFrame()

    def aggregate(self, name: str, group_by: str, measure: str, agg_func='sum'):
        df = self.datasets.get(name)
        if df is not None and group_by in df.columns and measure in df.columns:
            return df.groupby(group_by)[measure].agg(agg_func).reset_index()
        return pd.DataFrame()
