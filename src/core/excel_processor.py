import pandas as pd

class ExcelProcessor:
    def __init__(self):
        self.files = {}
    
    def load_files(self, file_paths):
        for path in file_paths:
            try:
                self.files[path] = pd.read_excel(path, sheet_name=None, engine='openpyxl')
            except Exception as e:
                print(f"Error loading {path}: {e}")
    
    def get_sheet_info(self):
        for path, sheets in self.files.items():
            print(f"\n File: {path}")
            for name, df in sheets.items():
                print(f"  - Sheet: {name}, Rows: {df.shape[0]}, Columns: {df.shape[1]}, Column Names: {list(df.columns)}")
    
    def preview_data(self, rows=5):
        for path, sheets in self.files.items():
            print(f"\n🔍 Preview from file: {path}")
            for name, df in sheets.items():
                print(f"   Sheet: {name}")
                print(df.head(rows))

# Example usage
if __name__ == "__main__":
    processor = ExcelProcessor()
    processor.load_files([
        "C:/Users/Hp/Downloads/financial-data-parser (1)/financial-data-parser/data/sample/KH_Bank.XLSX",
        "C:/Users/Hp/Downloads\financial-data-parser (1)/financial-data-parser/data/sample/Customer_Ledger_Entries_FULL.xlsx"
    ])
    processor.get_sheet_info()
    processor.preview_data()
